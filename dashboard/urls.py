from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('practice/', views.practice_questions, name='practice'),
    path('mock-test/', views.mock_test, name='mock_test'),
    path('submit-test/', views.submit_test, name='submit_test'),
    path('progress/', views.progress_tracker, name='progress'),
    path('bookmarks/', views.bookmarks_view, name='bookmarks'),
    path('bookmark/<int:question_id>/', views.toggle_bookmark, name='toggle_bookmark'),
    path('study-planner/', views.study_planner, name='study_planner'),
    path('update-progress/', views.update_practice_progress, name='update_progress'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('search/', views.search, name='search'),
]
