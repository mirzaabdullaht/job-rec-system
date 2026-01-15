"""
Script to seed the database with comprehensive job listings
Run: python manage.py shell < seed_jobs.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from accounts.models import Job, Category, Skill
from django.utils import timezone

# Create categories if they don't exist
categories_data = [
    "Software Development",
    "Data Science",
    "DevOps & Cloud",
    "UI/UX Design",
    "Digital Marketing",
    "Cybersecurity",
    "Mobile Development",
    "Project Management"
]

categories = {}
for cat_name in categories_data:
    cat, _ = Category.objects.get_or_create(name=cat_name)
    categories[cat_name] = cat
    print(f"✓ Category: {cat_name}")

# Create skills if they don't exist
skills_data = [
    "Python", "JavaScript", "Java", "C++", "React", "Angular", "Vue.js",
    "Django", "Flask", "Node.js", "Spring Boot", "SQL", "MongoDB",
    "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Jenkins",
    "Git", "Agile", "Scrum", "Machine Learning", "Deep Learning",
    "TensorFlow", "PyTorch", "Pandas", "NumPy", "Scikit-learn",
    "HTML", "CSS", "TypeScript", "REST API", "GraphQL",
    "Microservices", "CI/CD", "Linux", "Bash", "PowerShell",
    "Figma", "Adobe XD", "Photoshop", "Illustrator", "Sketch",
    "SEO", "Google Analytics", "Content Marketing", "Social Media",
    "Penetration Testing", "Network Security", "CISSP", "Ethical Hacking"
]

skills = {}
for skill_name in skills_data:
    skill, _ = Skill.objects.get_or_create(name=skill_name)
    skills[skill_name] = skill

print(f"✓ Created {len(skills_data)} skills")

# Comprehensive job listings
jobs_data = [
    {
        "title": "Senior Python Developer",
        "company_name": "TechCorp Solutions",
        "location": "New York, NY",
        "job_type": "Full-time",
        "description": "We're seeking an experienced Python developer to join our backend team. You'll work on scalable microservices and APIs.",
        "requirements": "5+ years Python, Django/Flask, REST APIs, SQL, Docker. Experience with AWS preferred.",
        "salary_min": 120000,
        "salary_max": 150000,
        "category": categories["Software Development"],
        "is_active": True
    },
    {
        "title": "Full Stack JavaScript Engineer",
        "company_name": "StartupHub Inc",
        "location": "San Francisco, CA",
        "job_type": "Full-time",
        "description": "Join our agile team building modern web applications. Work with React, Node.js, and MongoDB in a fast-paced environment.",
        "requirements": "3+ years JavaScript, React, Node.js, MongoDB, Git. TypeScript experience is a plus.",
        "salary_min": 100000,
        "salary_max": 140000,
        "category": categories["Software Development"],
        "is_active": True
    },
    {
        "title": "Data Scientist - ML Engineer",
        "company_name": "DataDriven Analytics",
        "location": "Boston, MA",
        "job_type": "Full-time",
        "description": "Build and deploy machine learning models for predictive analytics. Work with large datasets and cutting-edge ML frameworks.",
        "requirements": "Master's in CS/Stats, Python, TensorFlow/PyTorch, Pandas, SQL, statistical modeling experience.",
        "salary_min": 130000,
        "salary_max": 170000,
        "category": categories["Data Science"],
        "is_active": True
    },
    {
        "title": "Junior Data Analyst",
        "company_name": "RetailMetrics Co",
        "location": "Chicago, IL",
        "job_type": "Full-time",
        "description": "Analyze customer data and create visualizations. Entry-level position with mentorship opportunities.",
        "requirements": "Bachelor's degree, SQL, Excel, Python/R basics, data visualization tools (Tableau/PowerBI).",
        "salary_min": 60000,
        "salary_max": 75000,
        "category": categories["Data Science"],
        "is_active": True
    },
    {
        "title": "DevOps Engineer",
        "company_name": "CloudFirst Systems",
        "location": "Austin, TX",
        "job_type": "Full-time",
        "description": "Manage CI/CD pipelines and cloud infrastructure. Automate deployments and maintain high availability systems.",
        "requirements": "3+ years DevOps, AWS/Azure, Docker, Kubernetes, Jenkins, Terraform, scripting (Bash/Python).",
        "salary_min": 110000,
        "salary_max": 145000,
        "category": categories["DevOps & Cloud"],
        "is_active": True
    },
    {
        "title": "Cloud Architect",
        "company_name": "Enterprise Cloud Solutions",
        "location": "Seattle, WA",
        "job_type": "Full-time",
        "description": "Design and implement cloud solutions for enterprise clients. Lead cloud migration projects.",
        "requirements": "7+ years experience, AWS/Azure certification, microservices architecture, security best practices.",
        "salary_min": 150000,
        "salary_max": 190000,
        "category": categories["DevOps & Cloud"],
        "is_active": True
    },
    {
        "title": "UI/UX Designer",
        "company_name": "Creative Digital Agency",
        "location": "Los Angeles, CA",
        "job_type": "Full-time",
        "description": "Create beautiful and intuitive user interfaces. Conduct user research and usability testing.",
        "requirements": "3+ years UI/UX design, Figma/Adobe XD, user research, prototyping, HTML/CSS knowledge preferred.",
        "salary_min": 85000,
        "salary_max": 115000,
        "category": categories["UI/UX Design"],
        "is_active": True
    },
    {
        "title": "Product Designer",
        "company_name": "FinTech Innovators",
        "location": "Remote",
        "job_type": "Full-time",
        "description": "Design end-to-end product experiences for financial applications. Collaborate with product managers and engineers.",
        "requirements": "5+ years product design, design systems, Figma, user testing, mobile-first design.",
        "salary_min": 100000,
        "salary_max": 135000,
        "category": categories["UI/UX Design"],
        "is_active": True
    },
    {
        "title": "Digital Marketing Manager",
        "company_name": "Growth Marketing Pro",
        "location": "Miami, FL",
        "job_type": "Full-time",
        "description": "Lead digital marketing campaigns across channels. Optimize SEO, PPC, and social media strategies.",
        "requirements": "4+ years digital marketing, SEO, Google Analytics, content marketing, social media management.",
        "salary_min": 75000,
        "salary_max": 95000,
        "category": categories["Digital Marketing"],
        "is_active": True
    },
    {
        "title": "SEO Specialist",
        "company_name": "WebTraffic Solutions",
        "location": "Remote",
        "job_type": "Part-time",
        "description": "Improve website rankings and organic traffic. Conduct keyword research and technical SEO audits.",
        "requirements": "2+ years SEO experience, Google Analytics, keyword research tools, content optimization.",
        "salary_min": 40000,
        "salary_max": 55000,
        "category": categories["Digital Marketing"],
        "is_active": True
    },
    {
        "title": "Cybersecurity Analyst",
        "company_name": "SecureNet Corporation",
        "location": "Washington, DC",
        "job_type": "Full-time",
        "description": "Monitor security threats and respond to incidents. Perform vulnerability assessments and penetration testing.",
        "requirements": "3+ years cybersecurity, Security+/CISSP certification, penetration testing, SIEM tools.",
        "salary_min": 95000,
        "salary_max": 125000,
        "category": categories["Cybersecurity"],
        "is_active": True
    },
    {
        "title": "iOS Developer",
        "company_name": "Mobile App Studios",
        "location": "San Diego, CA",
        "job_type": "Full-time",
        "description": "Build native iOS applications using Swift. Collaborate with designers to create smooth user experiences.",
        "requirements": "3+ years iOS development, Swift, SwiftUI, REST APIs, App Store submission experience.",
        "salary_min": 105000,
        "salary_max": 135000,
        "category": categories["Mobile Development"],
        "is_active": True
    },
    {
        "title": "React Native Developer",
        "company_name": "CrossPlatform Apps Inc",
        "location": "Remote",
        "job_type": "Contract",
        "description": "Develop cross-platform mobile applications. Work on both iOS and Android using React Native.",
        "requirements": "2+ years React Native, JavaScript/TypeScript, mobile UI patterns, Redux.",
        "salary_min": 90000,
        "salary_max": 120000,
        "category": categories["Mobile Development"],
        "is_active": True
    },
    {
        "title": "Technical Project Manager",
        "company_name": "Agile Software Group",
        "location": "Denver, CO",
        "job_type": "Full-time",
        "description": "Lead software development projects using Agile methodologies. Coordinate between teams and stakeholders.",
        "requirements": "5+ years project management, Agile/Scrum certification, Jira, technical background preferred.",
        "salary_min": 110000,
        "salary_max": 140000,
        "category": categories["Project Management"],
        "is_active": True
    },
    {
        "title": "Scrum Master",
        "company_name": "Enterprise Solutions Ltd",
        "location": "Philadelphia, PA",
        "job_type": "Full-time",
        "description": "Facilitate Scrum ceremonies and remove impediments. Coach teams on Agile best practices.",
        "requirements": "CSM certification, 3+ years Scrum Master experience, conflict resolution, team coaching.",
        "salary_min": 90000,
        "salary_max": 115000,
        "category": categories["Project Management"],
        "is_active": True
    },
    {
        "title": "Backend Java Developer",
        "company_name": "Financial Services Corp",
        "location": "Charlotte, NC",
        "job_type": "Full-time",
        "description": "Develop enterprise-grade backend systems using Java and Spring Boot. Work on payment processing systems.",
        "requirements": "4+ years Java, Spring Boot, microservices, SQL, Kafka, experience in financial services preferred.",
        "salary_min": 115000,
        "salary_max": 145000,
        "category": categories["Software Development"],
        "is_active": True
    },
    {
        "title": "Frontend React Developer",
        "company_name": "E-Commerce Platform",
        "location": "Portland, OR",
        "job_type": "Full-time",
        "description": "Build responsive e-commerce interfaces with React. Focus on performance optimization and user experience.",
        "requirements": "3+ years React, Redux, TypeScript, responsive design, performance optimization.",
        "salary_min": 95000,
        "salary_max": 125000,
        "category": categories["Software Development"],
        "is_active": True
    },
    {
        "title": "Machine Learning Intern",
        "company_name": "AI Research Lab",
        "location": "Palo Alto, CA",
        "job_type": "Internship",
        "description": "Work on cutting-edge ML research projects. Learn from senior ML engineers and data scientists.",
        "requirements": "Currently pursuing CS degree, Python, basic ML knowledge, TensorFlow/PyTorch coursework.",
        "salary_min": 30000,
        "salary_max": 40000,
        "category": categories["Data Science"],
        "is_active": True
    },
    {
        "title": "Penetration Tester",
        "company_name": "CyberDefense Consultants",
        "location": "Remote",
        "job_type": "Full-time",
        "description": "Conduct ethical hacking and security assessments. Identify vulnerabilities before malicious actors do.",
        "requirements": "CEH/OSCP certification, 3+ years penetration testing, Kali Linux, web application security.",
        "salary_min": 105000,
        "salary_max": 140000,
        "category": categories["Cybersecurity"],
        "is_active": True
    },
    {
        "title": "Content Marketing Writer",
        "company_name": "Digital Content Hub",
        "location": "Remote",
        "job_type": "Part-time",
        "description": "Create engaging blog posts and marketing content. SEO optimization and audience research.",
        "requirements": "2+ years content writing, SEO knowledge, WordPress, portfolio of published work.",
        "salary_min": 35000,
        "salary_max": 50000,
        "category": categories["Digital Marketing"],
        "is_active": True
    }
]

# Create jobs
created_count = 0
for job_data in jobs_data:
    job, created = Job.objects.get_or_create(
        title=job_data["title"],
        company_name=job_data["company_name"],
        defaults=job_data
    )
    if created:
        created_count += 1
        print(f"✓ Created: {job.title} at {job.company_name}")
    else:
        print(f"○ Exists: {job.title} at {job.company_name}")

print(f"\n✅ Total jobs created: {created_count}/{len(jobs_data)}")
print(f"✅ Total jobs in database: {Job.objects.count()}")
print(f"✅ Total categories: {Category.objects.count()}")
print(f"✅ Total skills: {Skill.objects.count()}")
print("\nSeeding complete! Visit http://127.0.0.1:8000/jobs/ to see the jobs.")
