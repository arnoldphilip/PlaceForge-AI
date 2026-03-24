from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    CATEGORY_CHOICES = [
        ('aptitude', 'Aptitude'),
        ('verbal', 'Verbal'),
        ('tech', 'Tech'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    icon = models.CharField(max_length=50, default='📚')
    total_questions = models.IntegerField(default=0)
    difficulty = models.CharField(max_length=20, default='Beginner')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.title}"

    def get_question_count(self):
        return self.questions.count()


class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    ANSWER_CHOICES = [
        ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'),
    ]

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500)
    option_d = models.CharField(max_length=500)
    correct_answer = models.CharField(max_length=1, choices=ANSWER_CHOICES)
    explanation = models.TextField(blank=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='easy')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Q: {self.text[:60]}..."

    def get_correct_option_text(self):
        mapping = {'A': self.option_a, 'B': self.option_b, 'C': self.option_c, 'D': self.option_d}
        return mapping.get(self.correct_answer, '')


class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='progress')
    questions_attempted = models.IntegerField(default=0)
    questions_correct = models.IntegerField(default=0)
    last_activity = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'course')

    @property
    def accuracy(self):
        if self.questions_attempted == 0:
            return 0
        return round((self.questions_correct / self.questions_attempted) * 100, 1)

    @property
    def percentage(self):
        """Progress bar fill percentage (based on question count in course)."""
        total = self.course.questions.count()
        if total == 0:
            return 0
        return min(round((self.questions_attempted / total) * 100), 100)

    def __str__(self):
        return f"{self.user.username} - {self.course.title}"


class MockTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mock_tests')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='mock_tests')
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)
    time_taken = models.IntegerField(default=0)  # seconds

    @property
    def percentage(self):
        if self.total_questions == 0:
            return 0
        return round(self.score / self.total_questions * 100)

    def __str__(self):
        return f"{self.user.username} - {self.course.title} - {self.score}/{self.total_questions}"


class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarks')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'question')

    def __str__(self):
        return f"{self.user.username} bookmarked Q#{self.question.id}"


class StudyPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_plans')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    scheduled_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.title}"
