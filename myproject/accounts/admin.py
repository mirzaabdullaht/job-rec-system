from django.contrib import admin
from .models import (
    Category,
    Profile,
    Education,
    Experience,
    Application,
    Bookmark,
    Notification,
    ActivityLog,
)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)




@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user",)
    search_fields = ("user__username", "user__email")
    filter_horizontal = ("skills",)


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("profile", "institution", "degree", "start_year", "end_year")
    search_fields = ("institution", "degree")


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("profile", "company", "role", "start_date", "end_date")
    search_fields = ("company", "role")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("user", "job", "status", "applied_at")
    list_filter = ("status",)
    search_fields = ("user__username", "job__title", "job__company_name")


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ("user", "job", "created_at")
    search_fields = ("user__username", "job__title")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "message", "created_at", "read")
    list_filter = ("read",)
    search_fields = ("user__username", "message")


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "user", "action")
    search_fields = ("action", "user__username")
