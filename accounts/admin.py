from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('bio', 'level', 'points', 'streak_days', 'avatar')


class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'points', 'streak_days', 'created_at')
    list_filter = ('level',)
    search_fields = ('user__username', 'user__email')
    list_editable = ('points', 'level')
    ordering = ('-points',)

    fieldsets = (
        ('User Info', {'fields': ('user', 'bio', 'avatar')}),
        ('Progress', {'fields': ('level', 'points', 'streak_days')}),
    )
