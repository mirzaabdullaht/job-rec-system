# jobAccess/models.py - Job and Skills Models

from django.db import models
from django.contrib.auth.models import User

# Model for Skills
class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Model to link Users to their Skills
class UserSkill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'skill')

    def __str__(self):
        return f"{self.user.username} - {self.skill.name}"


# Job Category Model
class JobCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        verbose_name_plural = "Job Categories"
    
    def __str__(self):
        return self.name


# Job Model
class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Contract', 'Contract'),
        ('Internship', 'Internship'),
    ]

    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='jobs')
    posted_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  # Status of the job posting
    salary_min = models.IntegerField(null=True, blank=True)  # Minimum salary
    salary_max = models.IntegerField(null=True, blank=True)  # Maximum salary
    # Skills required for the job
    required_skills = models.ManyToManyField(Skill, related_name='jobs')

    def __str__(self):
        return f"{self.title} at {self.company_name}"

# Model for Job Recommendations
# This could be populated by your recommendation algorithm
class JobRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    # A score indicating how good the match is
    relevance_score = models.FloatField()
    # When the recommendation was generated
    generated_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-relevance_score'] # Show best recommendations first
        unique_together = ('user', 'job')

    def __str__(self):
        return f"Recommendation for {self.user.username}: {self.job.title}"
