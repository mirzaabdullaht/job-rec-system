# accounts/views.py
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db import models
from django.db.models import Q, Count
from jobAccess.models import Job, Skill, JobCategory
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

# -------------------- SIGNUP --------------------
@csrf_exempt
@require_POST
def signup_view(request):
    try:
        data = json.loads(request.body)
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if not username or not email or not password:
            return JsonResponse({"success": False, "error": "All fields are required."})

        if password != confirm_password:
            return JsonResponse({"success": False, "error": "Passwords do not match!"})

        if User.objects.filter(username=username).exists():
            return JsonResponse({"success": False, "error": "Username already taken."})

        if User.objects.filter(email=email).exists():
            return JsonResponse({"success": False, "error": "Email already registered."})

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        return JsonResponse({"success": True, "redirect_url": "/"})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


# -------------------- LOGIN --------------------
@csrf_exempt
@require_POST
def login_view(request):
    try:
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")

        try:
            user = User.objects.get(email=email)
            username = user.username
        except User.DoesNotExist:
            return JsonResponse({"success": False, "error": "Invalid email or password."})

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({"success": True, "redirect_url": "/"})
        else:
            return JsonResponse({"success": False, "error": "Invalid email or password."})

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


# -------------------- JOB APIs --------------------
@csrf_exempt
def jobs_collection(request):
    if request.method == "GET":
        # Filters
        q = request.GET.get("q", "").strip()
        job_type = request.GET.get("job_type")
        is_active = request.GET.get("is_active")
        category = request.GET.get("category")
        salary_min = request.GET.get("salary_min")
        salary_max = request.GET.get("salary_max")
        page = int(request.GET.get("page", 1))
        per_page = int(request.GET.get("per_page", 10))

        qs = Job.objects.all()
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(company_name__icontains=q) | Q(location__icontains=q) | Q(description__icontains=q))
        if job_type:
            qs = qs.filter(job_type=job_type)
        if is_active in ("true", "false"):
            qs = qs.filter(is_active=(is_active == "true"))
        if category:
            qs = qs.filter(category__name__iexact=category) | qs.filter(category__id=category)
        if salary_min:
            try:
                qs = qs.filter(salary_min__gte=salary_min)
            except Exception:
                pass
        if salary_max:
            try:
                qs = qs.filter(salary_max__lte=salary_max)
            except Exception:
                pass

        qs = qs.order_by("-posted_date")

        paginator = Paginator(qs, per_page)
        page_obj = paginator.get_page(page)

        items = []
        for job in page_obj.object_list:
            items.append({
                "id": job.id,
                "title": job.title,
                "company_name": job.company_name,
                "location": job.location,
                "job_type": job.job_type,
                "category": job.category.name if job.category else None,
                "is_active": job.is_active,
                "posted_date": job.posted_date.strftime("%Y-%m-%d"),
                "applications": job.applications.count(),
            })

        return JsonResponse({
            "items": items,
            "page": page_obj.number,
            "pages": paginator.num_pages,
            "total": paginator.count,
        })

    elif request.method == "POST":
        if not request.user.is_authenticated or not request.user.is_staff:
            return JsonResponse({"error": "Staff permission required"}, status=403)
        data = json.loads(request.body or "{}")
        cat = None
        cat_val = data.get("category")
        if cat_val:
            if isinstance(cat_val, int) or str(cat_val).isdigit():
                cat = Category.objects.filter(id=int(cat_val)).first()
            else:
                cat, _ = Category.objects.get_or_create(name=str(cat_val).strip())
        job = Job.objects.create(
            title=data.get("title", ""),
            company_name=data.get("company_name", ""),
            location=data.get("location", ""),
            job_type=data.get("job_type", "Full-time"),
            description=data.get("description", ""),
            salary_min=data.get("salary_min") or None,
            salary_max=data.get("salary_max") or None,
            is_active=bool(data.get("is_active", True)),
            category=cat,
        )
        return JsonResponse({"success": True, "id": job.id})

    return HttpResponseNotAllowed(["GET", "POST"])


@csrf_exempt
def job_detail(request, job_id):
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

    if request.method == "GET":
        return JsonResponse({
            "id": job.id,
            "title": job.title,
            "company_name": job.company_name,
            "location": job.location,
            "job_type": job.job_type,
            "description": job.description,
            "salary_min": str(job.salary_min) if job.salary_min is not None else None,
            "salary_max": str(job.salary_max) if job.salary_max is not None else None,
            "is_active": job.is_active,
            "posted_date": job.posted_date.strftime("%Y-%m-%d"),
            "category": job.category.name if job.category else None,
            "applications": job.applications.count(),
        })
    elif request.method in ("PUT", "PATCH"):
        if not request.user.is_authenticated or not request.user.is_staff:
            return JsonResponse({"error": "Staff permission required"}, status=403)
        data = json.loads(request.body or "{}")
        for field in [
            "title", "company_name", "location", "job_type", "description"
        ]:
            if field in data:
                setattr(job, field, data[field])
        if "salary_min" in data:
            job.salary_min = data["salary_min"] or None
        if "salary_max" in data:
            job.salary_max = data["salary_max"] or None
        if "is_active" in data:
            job.is_active = bool(data["is_active"])
        if "category" in data:
            cat_val = data.get("category")
            if not cat_val:
                job.category = None
            else:
                if isinstance(cat_val, int) or str(cat_val).isdigit():
                    job.category = JobCategory.objects.filter(id=int(cat_val)).first()
                else:
                    job.category, _ = JobCategory.objects.get_or_create(name=str(cat_val).strip())
        job.save()
        return JsonResponse({"success": True})
    elif request.method == "DELETE":
        if not request.user.is_authenticated or not request.user.is_staff:
            return JsonResponse({"error": "Staff permission required"}, status=403)
        job.delete()
        return JsonResponse({"success": True})

    return HttpResponseNotAllowed(["GET", "PUT", "PATCH", "DELETE"])

@csrf_exempt
def job_stats(request):
    try:
        total = Job.objects.count()
        active = Job.objects.filter(is_active=True).count()
        recent = Job.objects.order_by("-posted_date")[:5].count()
        applications = Application.objects.count()
        bookmarks = Bookmark.objects.count()
        total_users = User.objects.count()
        by_category = (
            Job.objects.values("category__name").annotate(c=Count("id")).order_by("-c")
        )
        return JsonResponse({
            "totalJobs": total,
            "activeJobs": active,
            "recentJobs": recent,
            "totalApplications": applications,
            "totalBookmarks": bookmarks,
            "totalUsers": total_users,
            "jobsByCategory": [
                {"category": r["category__name"] or "Uncategorized", "count": r["c"]}
                for r in by_category
            ],
        })
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# -------------------- APPLICATIONS & BOOKMARKS --------------------
@csrf_exempt
def apply_to_job(request, job_id):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

    try:
        application, created = Application.objects.get_or_create(user=request.user, job=job)
    except Exception as exc:
        return JsonResponse({"error": str(exc)}, status=500)

    if created:
        ActivityLog.objects.create(user=request.user, action="apply", meta={"job_id": job.id})
        Notification.objects.create(user=request.user, message=f"Applied to {job.title}")

        staff_users = User.objects.filter(is_staff=True).exclude(id=request.user.id)
        staff_notifications = [
            Notification(user=staff, message=f"{request.user.username} applied to {job.title}")
            for staff in staff_users
        ]
        if staff_notifications:
            Notification.objects.bulk_create(staff_notifications)

    return JsonResponse({
        "success": True,
        "alreadyApplied": not created,
        "message": "Application recorded" if created else "Application already exists",
    })


@csrf_exempt
def bookmark_job(request, job_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)
    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

    if request.method == "POST":
        bookmark, created = Bookmark.objects.get_or_create(user=request.user, job=job)
        ActivityLog.objects.create(user=request.user, action="bookmark", meta={"job_id": job.id})
        if created:
            Notification.objects.create(user=request.user, message=f"Bookmarked {job.title}")
        return JsonResponse({"success": True})
    elif request.method == "DELETE":
        Bookmark.objects.filter(user=request.user, job=job).delete()
        ActivityLog.objects.create(user=request.user, action="unbookmark", meta={"job_id": job.id})
        return JsonResponse({"success": True})
    return HttpResponseNotAllowed(["POST", "DELETE"])


@csrf_exempt
def list_bookmarks(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)
    data = [
        {
            "id": b.job.id,
            "title": b.job.title,
            "company_name": b.job.company_name,
            "location": b.job.location,
            "job_type": b.job.job_type,
        }
        for b in Bookmark.objects.select_related("job").filter(user=request.user)
    ]
    return JsonResponse({"items": data})


@csrf_exempt
def list_applications(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)
    data = [
        {
            "id": a.job.id,
            "title": a.job.title,
            "company_name": a.job.company_name,
            "status": a.status,
            "applied_at": a.applied_at.strftime("%Y-%m-%d"),
        }
        for a in Application.objects.select_related("job").filter(user=request.user).order_by("-applied_at")
    ]
    return JsonResponse({"items": data})


# -------------------- PROFILE --------------------
def ensure_profile(user):
    profile, _ = Profile.objects.get_or_create(user=user)
    return profile


@csrf_exempt
def profile_endpoint(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)
    profile = ensure_profile(request.user)

    if request.method == "GET":
        return JsonResponse({
            "user": request.user.username,
            "bio": profile.bio or "",
            "resume": profile.resume.url if profile.resume else None,
            "skills": [s.name for s in profile.skills.all()],
            "education": [
                {"institution": e.institution, "degree": e.degree, "start_year": e.start_year, "end_year": e.end_year}
                for e in profile.education.all()
            ],
            "experience": [
                {"company": x.company, "role": x.role, "start_date": str(x.start_date) if x.start_date else None, "end_date": str(x.end_date) if x.end_date else None}
                for x in profile.experience.all()
            ],
        })
    elif request.method in ("PUT", "PATCH"):
        data = json.loads(request.body or "{}")
        if "bio" in data:
            profile.bio = data.get("bio") or ""
        if "skills" in data and isinstance(data["skills"], list):
            skill_objs = []
            for name in data["skills"]:
                if not name:
                    continue
                s, _ = Skill.objects.get_or_create(name=str(name).strip())
                skill_objs.append(s)
            profile.save()
            profile.skills.set(skill_objs)
        profile.save()
        ActivityLog.objects.create(user=request.user, action="profile_update")
        return JsonResponse({"success": True})
    return HttpResponseNotAllowed(["GET", "PUT", "PATCH"])


@csrf_exempt
def profile_resume_upload(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)
    profile = ensure_profile(request.user)
    f = request.FILES.get("resume")
    if not f:
        return JsonResponse({"error": "Missing file 'resume'"}, status=400)
    profile.resume = f
    profile.save()
    ActivityLog.objects.create(user=request.user, action="resume_upload")
    return JsonResponse({"success": True, "url": profile.resume.url})


@csrf_exempt
def profile_picture_upload(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)
    profile = ensure_profile(request.user)
    f = request.FILES.get("profile_picture")
    if not f:
        return JsonResponse({"error": "Missing file 'profile_picture'"}, status=400)
    profile.profile_picture = f
    profile.save()
    ActivityLog.objects.create(user=request.user, action="profile_picture_upload")
    return JsonResponse({"success": True, "url": profile.profile_picture.url})


# -------------------- NOTIFICATIONS --------------------
@csrf_exempt
def notifications_list(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)
    items = [
        {
            "id": n.id, 
            "message": n.message, 
            "created_at": n.created_at.isoformat(), 
            "read": n.read
        }
        for n in Notification.objects.filter(user=request.user).order_by("-created_at")
    ]
    return JsonResponse({"items": items})


@csrf_exempt
def notifications_mark_read(request, notif_id):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)
    Notification.objects.filter(id=notif_id, user=request.user).update(read=True)
    return JsonResponse({"success": True})


@csrf_exempt
def notifications_mark_read_bulk(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)
    try:
        data = json.loads(request.body)
        ids = data.get("ids", [])
        Notification.objects.filter(id__in=ids, user=request.user).update(read=True)
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


@csrf_exempt
def add_education(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)
    profile = ensure_profile(request.user)
    if request.method == "GET":
        items = [
            {"id": e.id, "institution": e.institution, "degree": e.degree, "start_year": e.start_year, "end_year": e.end_year}
            for e in Education.objects.filter(profile=profile)
        ]
        return JsonResponse({"items": items})
    elif request.method == "POST":
        data = json.loads(request.body or "{}")
        try:
            Education.objects.create(
                profile=profile,
                institution=data.get("institution", ""),
                degree=data.get("degree", ""),
                start_year=data.get("start_year") and int(data["start_year"]) or None,
                end_year=data.get("end_year") and int(data["end_year"]) or None,
            )
            ActivityLog.objects.create(user=request.user, action="add_education")
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return HttpResponseNotAllowed(["GET", "POST"])


@csrf_exempt
def add_experience(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Authentication required"}, status=401)
    profile = ensure_profile(request.user)
    if request.method == "GET":
        items = [
            {"id": x.id, "company": x.company, "role": x.role, "start_date": str(x.start_date) if x.start_date else None, "end_date": str(x.end_date) if x.end_date else None, "description": x.description}
            for x in Experience.objects.filter(profile=profile)
        ]
        return JsonResponse({"items": items})
    elif request.method == "POST":
        data = json.loads(request.body or "{}")
        try:
            Experience.objects.create(
                profile=profile,
                company=data.get("company", ""),
                role=data.get("role", ""),
                start_date=data.get("start_date") or None,
                end_date=data.get("end_date") or None,
                description=data.get("description", ""),
            )
            ActivityLog.objects.create(user=request.user, action="add_experience")
            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return HttpResponseNotAllowed(["GET", "POST"])


def education_endpoint(request):
    return add_education(request)


def experience_endpoint(request):
    return add_experience(request)
