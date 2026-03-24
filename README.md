# 🚀 PlaceForge AI

An AI-powered exam preparation portal with Ollama Llama3 integration.

## Features
- 📚 Practice Questions (Aptitude, Verbal, Tech) with instant green/red feedback
- 📝 Timed Mock Tests with result modal
- 🤖 AI Assistant powered by local Ollama Llama3
- 📈 Progress tracking & leaderboard
- 🔖 Bookmarks, Study Planner
- 🛠️ Full Django Admin panel

## Setup & Run

### 1. Prerequisites
- Python 3.9+
- [Ollama](https://ollama.com) installed with llama3 model

### 2. Install Ollama & Pull Llama3
```bash
# Install Ollama from https://ollama.com
ollama pull llama3
ollama serve   # Start on localhost:11434
```

### 3. Setup Django
```bash
cd placeforge_ai
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data          # Seeds 36 sample questions
python manage.py createsuperuser    # Create admin account
python manage.py runserver
```

### 4. Access
- App: http://127.0.0.1:8000
- Admin: http://127.0.0.1:8000/admin

## Adding Questions via Admin
1. Go to `/admin/` → Courses → Add Course
2. Go to `/admin/` → Questions → Add Question
3. Set `correct_answer` to A, B, C or D exactly

## Notes
- If Ollama is not running, the chatbot falls back to rule-based responses
- `TIME_ZONE = 'Asia/Kolkata'` is already configured in settings.py
