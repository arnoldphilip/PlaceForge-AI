from django.contrib import admin
from django.utils.html import format_html
from .models import Course, Question, Progress, MockTest, Bookmark, StudyPlan


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 3
    fields = ('text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer', 'difficulty', 'explanation')
    show_change_link = True


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty', 'total_questions', 'icon', 'created_at')
    list_filter = ('category', 'difficulty')
    search_fields = ('title', 'description')
    inlines = [QuestionInline]
    list_editable = ('difficulty', 'icon')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('short_text', 'course', 'difficulty', 'correct_answer', 'created_at')
    list_filter = ('course__category', 'difficulty', 'correct_answer')
    search_fields = ('text', 'option_a', 'option_b', 'option_c', 'option_d')
    list_editable = ('difficulty', 'correct_answer')
    ordering = ('-created_at',)

    def short_text(self, obj):
        return obj.text[:80] + '...' if len(obj.text) > 80 else obj.text
    short_text.short_description = 'Question'

    fieldsets = (
        ('Question', {'fields': ('course', 'text', 'difficulty')}),
        ('Options', {
            'fields': ('option_a', 'option_b', 'option_c', 'option_d', 'correct_answer'),
            'description': 'Enter A, B, C, or D as the correct answer.'
        }),
        ('Explanation', {'fields': ('explanation',), 'classes': ('collapse',)}),
    )


@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'questions_attempted', 'questions_correct', 'accuracy_display')
    list_filter = ('course__category',)
    search_fields = ('user__username', 'course__title')

    def accuracy_display(self, obj):
        acc = obj.accuracy
        color = '#16a34a' if acc >= 70 else '#d97706' if acc >= 40 else '#dc2626'
        return format_html('<span style="color:{};font-weight:600;">{}%</span>', color, acc)
    accuracy_display.short_description = 'Accuracy'


@admin.register(MockTest)
class MockTestAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'score_display', 'time_taken_display', 'completed_at')
    list_filter = ('course__category', 'completed_at')
    search_fields = ('user__username',)
    ordering = ('-completed_at',)

    def score_display(self, obj):
        pct = round(obj.score / obj.total_questions * 100) if obj.total_questions else 0
        color = '#16a34a' if pct >= 70 else '#d97706' if pct >= 40 else '#dc2626'
        return format_html('<span style="color:{};font-weight:600;">{}/{} ({}%)</span>', color, obj.score, obj.total_questions, pct)
    score_display.short_description = 'Score'

    def time_taken_display(self, obj):
        mins = obj.time_taken // 60
        secs = obj.time_taken % 60
        return f'{mins}m {secs}s'
    time_taken_display.short_description = 'Time'


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ('user', 'question_short', 'created_at')
    search_fields = ('user__username',)

    def question_short(self, obj):
        return str(obj.question)[:60]
    question_short.short_description = 'Question'


@admin.register(StudyPlan)
class StudyPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'course', 'scheduled_date', 'is_completed')
    list_filter = ('is_completed', 'scheduled_date')
    search_fields = ('user__username', 'title')
    list_editable = ('is_completed',)
