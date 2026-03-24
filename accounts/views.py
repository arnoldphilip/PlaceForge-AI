from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views import View
from .models import UserProfile


class LoginView(View):
    """Handle user login."""
    template_name = 'accounts/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard:home')
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('dashboard:home')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, self.template_name, {'username': username})


class SignupView(View):
    """Handle user registration."""
    template_name = 'accounts/signup.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard:home')
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, self.template_name)

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, self.template_name)

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, self.template_name)

        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password1
        )
        profile = UserProfile.objects.create(user=user)
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
            profile.save()
        
        login(request, user)
        messages.success(request, f'Welcome to PlaceForge AI, {first_name}!')
        return redirect('dashboard:home')


class LogoutView(View):
    """Handle user logout."""
    def post(self, request):
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('main:home')


@login_required
def profile_view(request):
    """Display and update user profile."""
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()

        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']

        profile.bio = request.POST.get('bio', profile.bio)
        profile.level = request.POST.get('level', profile.level)
        profile.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect(request.POST.get('next', 'accounts:profile'))

    return render(request, 'accounts/profile.html', {'profile': profile})
