from django.core.management.base import BaseCommand
from jobAccess.models import Job, Skill
from accounts.models import Category


class Command(BaseCommand):
    help = 'Seed the database with sample jobs and skills'

    def handle(self, *args, **options):
        # Create sample skills
        skills_data = ["Python", "JavaScript", "React", "Django", "AWS", "Docker", "SQL", "Java", "Kubernetes"]
        for skill_name in skills_data:
            Skill.objects.get_or_create(name=skill_name)
            self.stdout.write(f"✓ Skill: {skill_name}")

        # Create sample category
        category, _ = Category.objects.get_or_create(name="Software Development")
        self.stdout.write(f"✓ Category: Software Development")

        # Create sample jobs
        jobs_data = [
            {
                "title": "Senior Python Developer",
                "company_name": "Tech Corp",
                "location": "San Francisco, CA",
                "description": "Looking for an experienced Python developer with Django expertise",
                "job_type": "Full-time",
                "is_active": True,
                "salary_min": 120000,
                "salary_max": 180000,
            },
            {
                "title": "React Developer",
                "company_name": "StartUp Inc",
                "location": "New York, NY",
                "description": "Build amazing web applications with React and JavaScript",
                "job_type": "Full-time",
                "is_active": True,
                "salary_min": 100000,
                "salary_max": 150000,
            },
            {
                "title": "DevOps Engineer",
                "company_name": "Cloud Systems",
                "location": "Remote",
                "description": "Manage cloud infrastructure using Docker and Kubernetes",
                "job_type": "Full-time",
                "is_active": True,
                "salary_min": 130000,
                "salary_max": 170000,
            },
            {
                "title": "Full Stack Developer",
                "company_name": "Web Solutions",
                "location": "Austin, TX",
                "description": "Create responsive web applications using React and Django",
                "job_type": "Full-time",
                "is_active": True,
                "salary_min": 110000,
                "salary_max": 160000,
            },
            {
                "title": "Data Analyst",
                "company_name": "Analytics Pro",
                "location": "Boston, MA",
                "description": "Analyze complex datasets and create reports",
                "job_type": "Full-time",
                "is_active": True,
                "salary_min": 90000,
                "salary_max": 130000,
            },
            {
                "title": "Java Backend Developer",
                "company_name": "Enterprise Solutions",
                "location": "Chicago, IL",
                "description": "Build scalable backend systems with Java",
                "job_type": "Full-time",
                "is_active": True,
                "salary_min": 115000,
                "salary_max": 155000,
            },
        ]

        for job_data in jobs_data:
            job, created = Job.objects.get_or_create(
                title=job_data["title"],
                company_name=job_data["company_name"],
                defaults={
                    "location": job_data["location"],
                    "description": job_data["description"],
                    "job_type": job_data["job_type"],
                    "is_active": job_data["is_active"],
                    "salary_min": job_data["salary_min"],
                    "salary_max": job_data["salary_max"],
                }
            )
            if created:
                self.stdout.write(f"✓ Created job: {job.title}")
                # Add skills to job
                job.required_skills.set(Skill.objects.all()[:5])
            else:
                self.stdout.write(f"✓ Job already exists: {job.title}")

        self.stdout.write(self.style.SUCCESS('✓ Data seeding complete!'))
