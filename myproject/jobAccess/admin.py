from django.contrib import admin
from .models import Skill, UserSkill, Job, JobCategory, JobRecommendation

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ("user", "skill")

@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ("title", "company_name", "location", "job_type", "category", "posted_date")
    search_fields = ("title", "company_name", "location")
    list_filter = ("job_type", "category")

@admin.register(JobRecommendation)
class JobRecommendationAdmin(admin.ModelAdmin):
    list_display = ("user", "job", "relevance_score", "generated_date")
    list_filter = ("generated_date",)

