import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Sum
from django.utils import timezone
from .models import Course, Question, Progress, MockTest, Bookmark, StudyPlan
from accounts.models import UserProfile


@login_required
def dashboard_home(request):
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)
    courses = Course.objects.all()
    progress_data = []
    for course in courses:
        prog, _ = Progress.objects.get_or_create(user=user, course=course)
        progress_data.append({'course': course, 'progress': prog})
    recent_tests = MockTest.objects.filter(user=user).order_by('-completed_at')[:5]
    total_attempted = Progress.objects.filter(user=user).aggregate(total=Sum('questions_attempted'))['total'] or 0
    total_correct = Progress.objects.filter(user=user).aggregate(total=Sum('questions_correct'))['total'] or 0
    upcoming_plans = StudyPlan.objects.filter(user=user, scheduled_date__gte=timezone.now().date(), is_completed=False).order_by('scheduled_date')[:3]
    leaderboard_data = UserProfile.objects.select_related('user').order_by('-points')[:10]
    context = {
        'profile': profile,
        'progress_data': progress_data,
        'recent_tests': recent_tests,
        'total_attempted': total_attempted,
        'total_correct': total_correct,
        'accuracy': round((total_correct / total_attempted * 100), 1) if total_attempted > 0 else 0,
        'upcoming_plans': upcoming_plans,
        'leaderboard': leaderboard_data,
        'active_tab': 'dashboard',
    }
    return render(request, 'dashboard/home.html', context)


@login_required
def practice_questions(request):
    category = request.GET.get('category', 'aptitude')
    difficulty = request.GET.get('difficulty', '')
    questions = Question.objects.filter(course__category=category)
    if difficulty:
        questions = questions.filter(difficulty=difficulty)

    # Get bookmarked question IDs for this user
    bookmarked_ids = set(
        Bookmark.objects.filter(user=request.user).values_list('question_id', flat=True)
    )

    context = {
        'questions': questions[:20],
        'category': category,
        'difficulty': difficulty,
        'bookmarked_ids': bookmarked_ids,
        'active_tab': 'practice',
    }
    return render(request, 'dashboard/practice.html', context)


@login_required
def mock_test(request):
    category = request.GET.get('category', 'aptitude')
    questions = list(Question.objects.filter(course__category=category).order_by('?')[:15])
    context = {
        'questions': questions,
        'category': category,
        'active_tab': 'mock_test',
    }
    return render(request, 'dashboard/mock_test.html', context)


@login_required
def submit_test(request):
    if request.method == 'POST':
        category = request.POST.get('category', 'aptitude')
        score = int(request.POST.get('score', 0))
        total = int(request.POST.get('total', 0))
        time_taken = int(request.POST.get('time_taken', 0))
        course = Course.objects.filter(category=category).first()
        if course:
            MockTest.objects.create(
                user=request.user, course=course,
                score=score, total_questions=total, time_taken=time_taken
            )
            prog, _ = Progress.objects.get_or_create(user=request.user, course=course)
            prog.questions_attempted += total
            prog.questions_correct += score
            prog.save()
            profile, _ = UserProfile.objects.get_or_create(user=request.user)
            profile.points += score * 10
            profile.save()
        pct = round(score / total * 100) if total else 0
        if pct >= 80:
            messages.success(request, f'Excellent! Score: {score}/{total} ({pct}%) 🎉')
        elif pct >= 50:
            messages.info(request, f'Good effort! Score: {score}/{total} ({pct}%)')
        else:
            messages.warning(request, f'Keep practicing! Score: {score}/{total} ({pct}%)')
    return redirect('dashboard:mock_test')


@login_required
def progress_tracker(request):
    progress_list = Progress.objects.filter(user=request.user).select_related('course')
    mock_tests = MockTest.objects.filter(user=request.user).order_by('-completed_at')[:10]
    context = {
        'progress_list': progress_list,
        'mock_tests': mock_tests,
        'active_tab': 'progress',
    }
    return render(request, 'dashboard/progress.html', context)


@login_required
def bookmarks_view(request):
    user_bookmarks = Bookmark.objects.filter(user=request.user).select_related('question__course')
    context = {'bookmarks': user_bookmarks, 'active_tab': 'bookmarks'}
    return render(request, 'dashboard/bookmarks.html', context)


@login_required
def toggle_bookmark(request, question_id):
    if request.method == 'POST':
        question = get_object_or_404(Question, id=question_id)
        bookmark, created = Bookmark.objects.get_or_create(user=request.user, question=question)
        if not created:
            bookmark.delete()
            return JsonResponse({'status': 'removed'})
        return JsonResponse({'status': 'added'})
    return JsonResponse({'error': 'Invalid'}, status=405)


@login_required
def study_planner(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '')
        scheduled_date = request.POST.get('scheduled_date')
        course_id = request.POST.get('course_id')
        if title and scheduled_date:
            course = Course.objects.filter(id=course_id).first()
            StudyPlan.objects.create(
                user=request.user, title=title,
                description=description, course=course,
                scheduled_date=scheduled_date
            )
            messages.success(request, 'Study plan added!')
        return redirect('dashboard:study_planner')

    if request.method == 'GET' and request.GET.get('complete'):
        plan_id = request.GET.get('complete')
        plan = get_object_or_404(StudyPlan, id=plan_id, user=request.user)
        plan.is_completed = not plan.is_completed
        plan.save()
        return redirect('dashboard:study_planner')

    plans = StudyPlan.objects.filter(user=request.user).order_by('scheduled_date')
    courses = Course.objects.all()
    context = {'plans': plans, 'courses': courses, 'active_tab': 'study_planner'}
    return render(request, 'dashboard/study_planner.html', context)


@login_required
@csrf_exempt
def update_practice_progress(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            category = data.get('category', 'aptitude')
            is_correct = data.get('is_correct', False)
            course = Course.objects.filter(category=category).first()
            points = 0
            if course:
                prog, _ = Progress.objects.get_or_create(user=request.user, course=course)
                prog.questions_attempted += 1
                if is_correct:
                    prog.questions_correct += 1
                    profile, _ = UserProfile.objects.get_or_create(user=request.user)
                    profile.points += 5
                    profile.save()
                    points = profile.points
                prog.save()
            return JsonResponse({'status': 'success', 'points': points})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=405)


@login_required
def leaderboard(request):
    top_users = UserProfile.objects.select_related('user').order_by('-points')[:20]
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    # Find user's rank
    user_rank = UserProfile.objects.filter(points__gt=user_profile.points).count() + 1
    context = {
        'top_users': top_users,
        'user_profile': user_profile,
        'user_rank': user_rank,
        'active_tab': 'leaderboard',
    }
    return render(request, 'dashboard/leaderboard.html', context)


@login_required
def search(request):
    query = request.GET.get('q', '').strip()
    questions = []
    courses = []
    if query:
        questions = Question.objects.filter(text__icontains=query)[:15]
        courses = Course.objects.filter(title__icontains=query)[:5]
    context = {'query': query, 'questions': questions, 'courses': courses}
    return render(request, 'dashboard/search.html', context)
