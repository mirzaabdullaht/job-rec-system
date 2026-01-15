from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model
from django.db.models import Q, Count
from jobAccess.models import Job, Skill
from accounts.models import Profile, Application, Bookmark, Notification

def index(request):
    # Show featured jobs on homepage
    featured_jobs = Job.objects.filter(is_active=True).order_by('-posted_date')[:6]
    return render(request, 'index.html', {'jobs': featured_jobs, 'user': request.user})

def about(request):
    return render(request, 'about.html', {'user': request.user})

def jobs(request):
    # List all active jobs
    job_list = Job.objects.filter(is_active=True).order_by('-posted_date')
    job_type = request.GET.get('job_type')
    location = request.GET.get('location')
    keyword = request.GET.get('keyword')
    salary_min = request.GET.get('salary_min')
    salary_max = request.GET.get('salary_max')
    
    if job_type and job_type != 'All':
        job_list = job_list.filter(job_type=job_type)
    if location:
        job_list = job_list.filter(location__icontains=location)
    if keyword:
        job_list = job_list.filter(
            Q(title__icontains=keyword) | 
            Q(description__icontains=keyword) | 
            Q(company_name__icontains=keyword)
        )
    if salary_min:
        try:
            job_list = job_list.filter(salary_min__gte=int(salary_min))
        except ValueError:
            pass
    if salary_max:
        try:
            job_list = job_list.filter(salary_max__lte=int(salary_max))
        except ValueError:
            pass
    
    return render(request, 'jobs.html', {'jobs': job_list, 'user': request.user})

def login(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'login.html')

@login_required
def user_profile(request):
    # Ensure profile
    profile, _ = Profile.objects.get_or_create(user=request.user)

    # Build smart recommendations based on user's skills, location, and job type preferences
    skill_names = list(profile.skills.values_list('name', flat=True))
    
    # Start with active jobs
    recommended_jobs = Job.objects.filter(is_active=True)
    
    # First, filter by skills if user has any
    if skill_names:
        skill_filter = Q()
        for skill in skill_names:
            skill_filter |= Q(title__icontains=skill) | Q(description__icontains=skill)
        recommended_jobs = recommended_jobs.filter(skill_filter)
    
    # Then order by posted date and limit
    recommended_jobs = recommended_jobs.order_by('-posted_date')[:6]
    
    # If we don't have enough recommendations, add more recent jobs
    if recommended_jobs.count() < 3:
        additional = Job.objects.filter(is_active=True).order_by('-posted_date').exclude(id__in=recommended_jobs.values_list('id', flat=True))[:6]
        recommended_jobs = list(recommended_jobs) + list(additional)

    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:5]

    return render(request, 'profile.html', {
        'user': request.user,
        'profile': profile,
        'recommended_jobs': recommended_jobs,
        'notifications': notifications,
    })

@login_required
def applications_page(request):
    """View user's job applications"""
    applications = Application.objects.filter(user=request.user).select_related('job').order_by('-applied_at')
    return render(request, 'applications.html', {
        'user': request.user,
        'applications': applications,
    })

@login_required
def admin_board(request):
    if not request.user.is_staff:
        return redirect('index')
    User = get_user_model()
    jobs_qs = Job.objects.order_by('-posted_date').annotate(app_count=Count('applications'))
    initial_jobs = list(jobs_qs[:25])

    stats = {
        'totalJobs': jobs_qs.count(),
        'activeJobs': jobs_qs.filter(is_active=True).count(),
        'totalApplications': Application.objects.count(),
        'totalBookmarks': Bookmark.objects.count(),
        'totalUsers': User.objects.count(),
    }

    jobs_payload = [
        {
            'id': job.id,
            'title': job.title,
            'company_name': job.company_name,
            'location': job.location,
            'job_type': job.job_type,
            'is_active': job.is_active,
            'applications': job.app_count,
            'posted_date': job.posted_date.strftime('%Y-%m-%d') if job.posted_date else None,
        }
        for job in initial_jobs
    ]

    context = {
        'user': request.user,
        'stats': stats,
        'initial_jobs': initial_jobs,
        'admin_preload': {
            'stats': stats,
            'jobs': jobs_payload,
        },
    }
    return render(request, 'admin_board.html', context)

def signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'signup.html')

def logout(request):
    auth_logout(request)
    return redirect('index')


@login_required
def bookmarks_page(request):
    items = Bookmark.objects.select_related('job').filter(user=request.user)
    jobs = [b.job for b in items]
    return render(request, 'bookmarks.html', { 'user': request.user, 'jobs': jobs })