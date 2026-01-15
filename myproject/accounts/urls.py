from django.urls import path
from . import views

urlpatterns = [
    # Auth APIs
    path("login/", views.login_view, name="api_login"),
    path("signup/", views.signup_view, name="api_signup"),
    
    # Admin board APIs
    path("api/jobs/", views.jobs_collection, name="jobs_collection"),
    path("api/jobs/<int:job_id>/", views.job_detail, name="job_detail"),
    path("api/stats/", views.job_stats, name="job_stats"),

    # Applications & Bookmarks
    path("api/jobs/<int:job_id>/apply/", views.apply_to_job, name="apply_to_job"),
    path("api/jobs/<int:job_id>/bookmark/", views.bookmark_job, name="bookmark_job"),
    path("api/bookmarks/", views.list_bookmarks, name="list_bookmarks"),
    path("api/applications/", views.list_applications, name="list_applications"),

    # Profile
    path("api/profile/", views.profile_endpoint, name="profile_endpoint"),
    path("api/profile/picture/", views.profile_picture_upload, name="profile_picture_upload"),
    path("api/profile/resume/", views.profile_resume_upload, name="profile_resume_upload"),
    path("api/profile/education/", views.education_endpoint, name="education_endpoint"),
    path("api/profile/experience/", views.experience_endpoint, name="experience_endpoint"),
    # Notifications
    path("api/notifications/", views.notifications_list, name="notifications_list"),
    path("api/notifications/mark-read/", views.notifications_mark_read_bulk, name="notifications_mark_read_bulk"),
    path("api/notifications/<int:notif_id>/read/", views.notifications_mark_read, name="notifications_mark_read"),
]