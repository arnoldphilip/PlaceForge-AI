import json
import requests
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ChatMessage

OLLAMA_SYSTEM_PROMPT = """You are PlaceForge AI, an expert tutor and learning assistant for a student preparation portal.

Your expertise covers:
- Aptitude: Quantitative reasoning, number systems, percentages, profit & loss, time & work, geometry, data interpretation, logical reasoning
- Verbal: Grammar, vocabulary, reading comprehension, sentence correction, para-jumbles, fill in the blanks
- Tech/Computer Science: Data Structures & Algorithms, Python, Java, JavaScript, Operating Systems, DBMS/SQL, Computer Networks, System Design, OOP, Web Development, Cloud Computing

Guidelines:
1. Give detailed, clear, step-by-step explanations with examples
2. For aptitude problems, show the full working/solution
3. For tech topics, include code examples where relevant
4. Be encouraging and educational
5. Format your response clearly with structure where appropriate
6. If asked a general knowledge question, answer it accurately and helpfully
7. Always be helpful - never refuse a genuine learning question"""


def get_fallback_response(message):
    msg_lower = message.lower()
    if any(w in msg_lower for w in ['hi', 'hello', 'hey', 'howdy']):
        return "Hello! I'm PlaceForge AI. I can help you with Aptitude, Verbal, and Tech topics. What would you like to learn today?"
    elif any(w in msg_lower for w in ['aptitude', 'math', 'arithmetic', 'percentage', 'profit', 'ratio', 'algebra']):
        return ("Aptitude covers quantitative and logical reasoning. Key areas:\n"
                "• Number Systems & HCF/LCM\n• Percentages & Ratio-Proportion\n"
                "• Profit & Loss, Simple/Compound Interest\n• Time, Speed & Distance\n"
                "• Data Interpretation\nPractice solving 10 problems daily to improve speed!")
    elif any(w in msg_lower for w in ['verbal', 'english', 'grammar', 'vocabulary', 'reading']):
        return ("Verbal ability tests your English proficiency. Focus areas:\n"
                "• Grammar rules (articles, tenses, prepositions)\n• Vocabulary building (synonyms/antonyms)\n"
                "• Reading Comprehension\n• Sentence Correction & Para-jumbles\nRead newspapers and novels daily!")
    elif any(w in msg_lower for w in ['python', 'java', 'javascript', 'code', 'programming', 'algorithm', 'database', 'sql', 'os', 'network']):
        return ("Tech topics for interviews typically include:\n"
                "• DSA: Arrays, Linked Lists, Trees, Graphs, Sorting, Searching\n"
                "• DBMS: SQL queries, normalization, transactions\n"
                "• OS: Process management, memory management, deadlocks\n"
                "• Computer Networks: TCP/IP, OSI model, HTTP/HTTPS\n"
                "• System Design: Scalability, caching, load balancing\n"
                "Which specific topic would you like to explore?")
    return ("I'm your PlaceForge AI assistant! I can help with:\n"
            "📊 Aptitude (math, reasoning, data interpretation)\n"
            "📖 Verbal (English, grammar, vocabulary)\n"
            "💻 Tech (programming, DSA, databases, OS)\n\n"
            "Note: For full AI responses, please ensure Ollama with llama3:8b is running on your machine.\n"
            "Ask me anything specific and I'll do my best to help!")


def get_ollama_response(message, history=None):
    """Connect to local Ollama llama3 with conversation context."""
    payload = {
        "model": "llama3:8b",
        "prompt": f"{OLLAMA_SYSTEM_PROMPT}\n\nUser: {message}\nAssistant:",
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 800,
        }
    }

    urls = [
        "http://localhost:11434/api/generate",
        "http://127.0.0.1:11434/api/generate",
    ]

    for url in urls:
        try:
            resp = requests.post(url, json=payload, timeout=60)
            if resp.status_code == 200:
                result = resp.json().get('response', '').strip()
                if result:
                    return result, True
        except requests.exceptions.ConnectionError:
            continue
        except requests.exceptions.Timeout:
            return "The AI is taking too long to respond. Please try a shorter question or check if Ollama is running.", False
        except Exception:
            continue

    return get_fallback_response(message), False


@login_required
def chatbot_page(request):
    messages_history = ChatMessage.objects.filter(user=request.user).order_by('-created_at')[:30]
    context = {
        'messages_history': reversed(list(messages_history)),
        'active_tab': 'chatbot',
    }
    return render(request, 'chatbot/chatbot.html', context)


@login_required
@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '').strip()
            if not user_message:
                return JsonResponse({'error': 'Empty message'}, status=400)

            bot_response, from_ollama = get_ollama_response(user_message)

            ChatMessage.objects.create(
                user=request.user,
                message=user_message,
                response=bot_response
            )

            return JsonResponse({
                'response': bot_response,
                'from_ai': from_ollama,
            })
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid method'}, status=405)


@login_required
def clear_chat(request):
    if request.method == 'POST':
        ChatMessage.objects.filter(user=request.user).delete()
        return JsonResponse({'status': 'cleared'})
    return JsonResponse({'error': 'Invalid'}, status=405)
