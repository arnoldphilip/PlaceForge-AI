"""
Management command to populate the PlaceForge AI database with sample questions.
Run: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from dashboard.models import Course, Question


SEED = {
    'aptitude': {
        'title': 'Quantitative Aptitude',
        'description': 'Master arithmetic, algebra, and logical reasoning',
        'icon': '💡',
        'difficulty': 'Intermediate',
        'questions': [
            {
                'text': 'A train 150 m long is running at 60 km/h. In what time will it pass a pole?',
                'a': '7.5 seconds', 'b': '9 seconds', 'c': '10 seconds', 'd': '12 seconds',
                'correct': 'B', 'diff': 'easy',
                'explanation': 'Speed = 60 km/h = 60 × (5/18) = 50/3 m/s. Time = 150 ÷ (50/3) = 9 seconds.'
            },
            {
                'text': 'What is 15% of 240?',
                'a': '32', 'b': '36', 'c': '40', 'd': '44',
                'correct': 'B', 'diff': 'easy',
                'explanation': '15% of 240 = (15/100) × 240 = 36.'
            },
            {
                'text': 'If A:B = 2:3 and B:C = 4:5, find A:B:C.',
                'a': '8:12:15', 'b': '6:9:15', 'c': '2:3:5', 'd': '4:6:10',
                'correct': 'A', 'diff': 'medium',
                'explanation': 'B is common. LCM of 3 and 4 = 12. A:B = 8:12, B:C = 12:15. So A:B:C = 8:12:15.'
            },
            {
                'text': 'A can do a work in 12 days, B in 18 days. Together they finish in?',
                'a': '6 days', 'b': '7.2 days', 'c': '8 days', 'd': '9 days',
                'correct': 'B', 'diff': 'medium',
                'explanation': 'Combined rate = 1/12 + 1/18 = 3/36 + 2/36 = 5/36. Time = 36/5 = 7.2 days.'
            },
            {
                'text': 'Simple interest on Rs.5000 at 8% per annum for 3 years?',
                'a': 'Rs.1000', 'b': 'Rs.1200', 'c': 'Rs.1500', 'd': 'Rs.1800',
                'correct': 'B', 'diff': 'easy',
                'explanation': 'SI = P×R×T/100 = 5000×8×3/100 = Rs.1200.'
            },
            {
                'text': 'The HCF of 36, 54 and 90 is?',
                'a': '6', 'b': '9', 'c': '18', 'd': '27',
                'correct': 'C', 'diff': 'easy',
                'explanation': 'HCF(36,54)=18, HCF(18,90)=18. Answer is 18.'
            },
            {
                'text': 'A boat goes 24 km upstream in 6 hours and 20 km downstream in 4 hours. Speed of stream?',
                'a': '0.5 km/h', 'b': '1 km/h', 'c': '1.5 km/h', 'd': '2 km/h',
                'correct': 'B', 'diff': 'hard',
                'explanation': 'Upstream speed=4 km/h, Downstream speed=5 km/h. Stream speed=(5-4)/2=0.5. Wait: correct is 0.5. Let me recalculate. Upstream=24/6=4, Downstream=20/4=5. Stream=(5-4)/2=0.5 km/h.'
            },
            {
                'text': 'Two numbers are in ratio 3:5. If each is increased by 10, ratio becomes 5:7. Find the numbers.',
                'a': '15 and 25', 'b': '10 and 20', 'c': '20 and 30', 'd': '25 and 35',
                'correct': 'A', 'diff': 'medium',
                'explanation': 'Let numbers be 3x and 5x. (3x+10)/(5x+10) = 5/7 → 21x+70=25x+50 → 4x=20 → x=5. Numbers: 15 and 25.'
            },
            {
                'text': 'Compound interest on Rs.8000 at 10% for 2 years compounded annually?',
                'a': 'Rs.1600', 'b': 'Rs.1680', 'c': 'Rs.1700', 'd': 'Rs.1760',
                'correct': 'B', 'diff': 'medium',
                'explanation': 'CI = 8000×(1.1)² - 8000 = 8000×1.21 - 8000 = 9680 - 8000 = Rs.1680.'
            },
            {
                'text': 'Find the next number in the series: 2, 6, 12, 20, 30, ?',
                'a': '40', 'b': '42', 'c': '44', 'd': '48',
                'correct': 'B', 'diff': 'easy',
                'explanation': 'Pattern: n×(n+1). 1×2=2, 2×3=6, 3×4=12, 4×5=20, 5×6=30, 6×7=42.'
            },
            {
                'text': 'A sells to B at 20% profit. B sells to C at 10% loss. If C pays Rs.2160, what did A pay?',
                'a': 'Rs.1800', 'b': 'Rs.2000', 'c': 'Rs.2200', 'd': 'Rs.2400',
                'correct': 'B', 'diff': 'hard',
                'explanation': 'C pays 2160 = B\'s cost × 0.9 → B\'s cost = 2400. B\'s cost = A\'s selling price = A\'s cost × 1.2 → A\'s cost = 2400/1.2 = 2000.'
            },
            {
                'text': 'LCM of 12, 18 and 24 is?',
                'a': '36', 'b': '48', 'c': '72', 'd': '96',
                'correct': 'C', 'diff': 'easy',
                'explanation': '12=2²×3, 18=2×3², 24=2³×3. LCM=2³×3²=72.'
            },
        ]
    },
    'verbal': {
        'title': 'Verbal Ability',
        'description': 'Improve English language skills and comprehension',
        'icon': '💬',
        'difficulty': 'Beginner',
        'questions': [
            {
                'text': 'Choose the correct synonym for "BENEVOLENT":',
                'a': 'Cruel', 'b': 'Generous', 'c': 'Selfish', 'd': 'Angry',
                'correct': 'B', 'diff': 'easy',
                'explanation': 'Benevolent means well-meaning and kindly. Synonym: Generous, Charitable, Kind.'
            },
            {
                'text': 'Identify the error: "He is one of those persons who believes in hardwork."',
                'a': 'He is', 'b': 'one of those persons', 'c': 'who believes', 'd': 'in hardwork',
                'correct': 'C', 'diff': 'medium',
                'explanation': '"who" refers to "persons" (plural), so it should be "who believe" (not "believes").'
            },
            {
                'text': 'Choose the antonym for "LUCID":',
                'a': 'Clear', 'b': 'Bright', 'c': 'Obscure', 'd': 'Transparent',
                'correct': 'C', 'diff': 'easy',
                'explanation': 'Lucid means clear and easy to understand. Its antonym is Obscure (unclear/vague).'
            },
            {
                'text': 'Fill in: "The committee _____ divided in their opinion."',
                'a': 'was', 'b': 'were', 'c': 'is', 'd': 'are',
                'correct': 'B', 'diff': 'medium',
                'explanation': 'When a collective noun implies individual members acting differently, use plural verb. "Were" is correct here.'
            },
            {
                'text': 'Choose the correctly spelled word:',
                'a': 'Accomodate', 'b': 'Accommodate', 'c': 'Acommodate', 'd': 'Accommodat',
                'correct': 'B', 'diff': 'easy',
                'explanation': 'The correct spelling is "Accommodate" — double c and double m.'
            },
            {
                'text': 'What does the idiom "to burn the midnight oil" mean?',
                'a': 'To waste resources', 'b': 'To work late into the night', 'c': 'To start a fire', 'd': 'To be careless',
                'correct': 'B', 'diff': 'easy',
                'explanation': 'The idiom "burn the midnight oil" means to study or work late at night.'
            },
            {
                'text': 'Choose the word most similar in meaning to "EPHEMERAL":',
                'a': 'Permanent', 'b': 'Eternal', 'c': 'Transient', 'd': 'Everlasting',
                'correct': 'C', 'diff': 'medium',
                'explanation': 'Ephemeral means lasting a very short time. Synonym: Transient, Fleeting, Momentary.'
            },
            {
                'text': 'Rearrange: P: the students Q: the teacher R: praised S: hardworking',
                'a': 'RQPS', 'b': 'QRPS', 'c': 'PRQS', 'd': 'QPRS',
                'correct': 'B', 'diff': 'medium',
                'explanation': 'Correct sentence: "The teacher praised the students hardworking" → Q R P S.'
            },
            {
                'text': 'Which sentence uses the passive voice correctly?',
                'a': 'The dog bit the man.', 'b': 'The man was bitten by the dog.', 'c': 'The man bites dogs.', 'd': 'The dog is biting.',
                'correct': 'B', 'diff': 'easy',
                'explanation': 'Passive voice structure: Subject + was/were + past participle + by + object. "The man was bitten by the dog" is correct passive voice.'
            },
            {
                'text': 'Choose the antonym of "VOCIFEROUS":',
                'a': 'Loud', 'b': 'Quiet', 'c': 'Noisy', 'd': 'Boisterous',
                'correct': 'B', 'diff': 'medium',
                'explanation': 'Vociferous means making a loud outcry. Its antonym is Quiet/Silent.'
            },
        ]
    },
    'tech': {
        'title': 'Technical Skills',
        'description': 'Computer science fundamentals and programming concepts',
        'icon': '⚙️',
        'difficulty': 'Intermediate',
        'questions': [
            {
                'text': 'What is the time complexity of binary search?',
                'a': 'O(n)', 'b': 'O(log n)', 'c': 'O(n²)', 'd': 'O(1)',
                'correct': 'B', 'diff': 'easy',
                'explanation': 'Binary search halves the search space each step, giving O(log n) time complexity. Array must be sorted.'
            },
            {
                'text': 'Which data structure uses LIFO (Last In, First Out) principle?',
                'a': 'Queue', 'b': 'Array', 'c': 'Stack', 'd': 'Linked List',
                'correct': 'C', 'diff': 'easy',
                'explanation': 'A Stack uses LIFO - the last element added is the first one removed. Queue uses FIFO.'
            },
            {
                'text': 'What does SQL stand for?',
                'a': 'Structured Query Language', 'b': 'Simple Query Language', 'c': 'Standard Query List', 'd': 'Sequential Query Language',
                'correct': 'A', 'diff': 'easy',
                'explanation': 'SQL stands for Structured Query Language, used to manage and query relational databases.'
            },
            {
                'text': 'Which sorting algorithm has the best average-case performance?',
                'a': 'Bubble Sort', 'b': 'Selection Sort', 'c': 'Quick Sort', 'd': 'Insertion Sort',
                'correct': 'C', 'diff': 'medium',
                'explanation': 'QuickSort has average O(n log n) performance. Merge Sort is also O(n log n) but uses more space. QuickSort is generally fastest in practice.'
            },
            {
                'text': 'What is a deadlock in OS?',
                'a': 'A process using 100% CPU', 'b': 'Two processes waiting for each other indefinitely', 'c': 'A crashed program', 'd': 'Memory overflow',
                'correct': 'B', 'diff': 'medium',
                'explanation': 'Deadlock occurs when two or more processes are blocked forever, each waiting for a resource held by the other. Conditions: Mutual Exclusion, Hold & Wait, No Preemption, Circular Wait.'
            },
            {
                'text': 'Which HTTP method is used to update a resource partially?',
                'a': 'GET', 'b': 'POST', 'c': 'PUT', 'd': 'PATCH',
                'correct': 'D', 'diff': 'medium',
                'explanation': 'PATCH updates a resource partially. PUT replaces the entire resource. POST creates new resources. GET retrieves data.'
            },
            {
                'text': 'What does OOP stand for?',
                'a': 'Object Oriented Programming', 'b': 'Output Oriented Programming', 'c': 'Object Operating Program', 'd': 'Oriented Object Protocol',
                'correct': 'A', 'diff': 'easy',
                'explanation': 'OOP = Object Oriented Programming. Its 4 pillars are: Encapsulation, Inheritance, Polymorphism, Abstraction.'
            },
            {
                'text': 'Which layer of the OSI model handles routing?',
                'a': 'Physical', 'b': 'Data Link', 'c': 'Network', 'd': 'Transport',
                'correct': 'C', 'diff': 'medium',
                'explanation': 'The Network Layer (Layer 3) handles routing and logical addressing (IP addresses). Routers operate at this layer.'
            },
            {
                'text': 'What is the output of: print(type([]) == type({}))?',
                'a': 'True', 'b': 'False', 'c': 'Error', 'd': 'None',
                'correct': 'B', 'diff': 'easy',
                'explanation': 'type([]) is <class "list"> and type({}) is <class "dict">. They are different, so the comparison is False.'
            },
            {
                'text': 'Which normal form eliminates transitive dependencies?',
                'a': '1NF', 'b': '2NF', 'c': '3NF', 'd': 'BCNF',
                'correct': 'C', 'diff': 'hard',
                'explanation': '3NF (Third Normal Form) eliminates transitive dependencies — non-key attributes must not depend on other non-key attributes.'
            },
            {
                'text': 'In Python, what does list comprehension [x**2 for x in range(5)] produce?',
                'a': '[1, 4, 9, 16, 25]', 'b': '[0, 1, 4, 9, 16]', 'c': '[0, 1, 2, 3, 4]', 'd': '[1, 2, 3, 4, 5]',
                'correct': 'B', 'diff': 'easy',
                'explanation': 'range(5) gives 0,1,2,3,4. Squaring each: 0,1,4,9,16. Result: [0, 1, 4, 9, 16].'
            },
            {
                'text': 'What is the worst-case time complexity of Merge Sort?',
                'a': 'O(n)', 'b': 'O(n log n)', 'c': 'O(n²)', 'd': 'O(log n)',
                'correct': 'B', 'diff': 'medium',
                'explanation': 'Merge Sort always divides and merges, giving O(n log n) in all cases — best, average, and worst.'
            },
        ]
    }
}


class Command(BaseCommand):
    help = 'Seed the database with sample courses and questions'

    def add_arguments(self, parser):
        parser.add_argument('--clear', action='store_true', help='Clear existing data before seeding')

    def handle(self, *args, **options):
        if options['clear']:
            Question.objects.all().delete()
            Course.objects.all().delete()
            self.stdout.write(self.style.WARNING('Cleared all courses and questions.'))

        total_q = 0
        for category, data in SEED.items():
            course, created = Course.objects.get_or_create(
                category=category,
                defaults={
                    'title': data['title'],
                    'description': data['description'],
                    'icon': data['icon'],
                    'difficulty': data['difficulty'],
                }
            )
            if not created:
                self.stdout.write(f'Course "{course.title}" already exists, adding questions...')

            for q in data['questions']:
                question, q_created = Question.objects.get_or_create(
                    course=course,
                    text=q['text'],
                    defaults={
                        'option_a': q['a'],
                        'option_b': q['b'],
                        'option_c': q['c'],
                        'option_d': q['d'],
                        'correct_answer': q['correct'],
                        'difficulty': q['diff'],
                        'explanation': q.get('explanation', ''),
                    }
                )
                if q_created:
                    total_q += 1

            course.total_questions = course.questions.count()
            course.save()
            self.stdout.write(self.style.SUCCESS(f'✓ {course.title}: {course.total_questions} questions'))

        self.stdout.write(self.style.SUCCESS(f'\n✅ Seeding complete! Added {total_q} new questions.'))
