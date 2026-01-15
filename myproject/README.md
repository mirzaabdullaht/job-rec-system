# Job Access Recommendation System

A full-featured Django web application for job posting and recommendation with admin panel integration.

## Features Implemented

### 🔐 User Authentication
- **Sign Up**: Create new user accounts with validation
- **Login**: Secure login with email and password
- **Logout**: Session management
- **Profile Page**: View user information and recommended jobs

### 💼 Job Management
- **Browse Jobs**: View all active job listings
- **Filter Jobs**: Filter by type, location, and keywords
- **Dynamic Job Cards**: Real-time data from database
- **Job Details**: Company name, location, salary, requirements

### 👨‍💼 Admin Panel (Staff Only)
- **Dashboard Statistics**: 
  - Total jobs count
  - Active jobs count
   - Total applications
   - Recent jobs
   - Total bookmarks
   - Jobs by category
- **CRUD Operations**:
  - ✅ Create new jobs
  - ✅ Edit existing jobs
  - ✅ Delete jobs
  - ✅ Toggle active/inactive status
- **Filters & Search**:
  - Search by job title, company, location
  - Filter by job type
  - Filter by status (active/inactive)
- **Real-time Updates**: Changes in Django admin instantly reflect in frontend admin panel

### 🔄 Integration
- **Backend ↔ Frontend Sync**: Any job added/edited in Django admin (`/admin/`) appears immediately in the frontend admin panel (`/admin_board/`)
- **REST API**: JSON endpoints for all job operations
- **Dynamic Templates**: Context-aware navigation showing user status

## Quick Start

### Prerequisites
- Python 3.12+
- Django 6.0.1

### Installation

```powershell
# Navigate to project directory
cd myproject

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser (staff account for admin access)
python manage.py createsuperuser
# Follow prompts to set username, email, and password

# Seed sample job data (optional but recommended)
python manage.py seed_jobs

# Run the development server
python manage.py runserver
```

### Access the Application

- **Homepage**: http://127.0.0.1:8000/
- **Browse Jobs**: http://127.0.0.1:8000/jobs/
- **Login**: http://127.0.0.1:8000/login/
- **Sign Up**: http://127.0.0.1:8000/signup/
- **User Profile**: http://127.0.0.1:8000/profile/ (requires login)
- **Frontend Admin Panel**: http://127.0.0.1:8000/admin_board/ (staff only)
- **Django Admin**: http://127.0.0.1:8000/admin/ (admin credentials required)

## Usage Workflows

### For Regular Users

1. **Sign Up**: Go to http://127.0.0.1:8000/signup/
   - Enter username, email, and password
   - Click "Sign Up"
   
2. **Login**: Go to http://127.0.0.1:8000/login/
   - Enter email and password
   - Click "Login"

3. **Browse Jobs**: Navigate to "Find Jobs"
   - See all available positions
   - Use filters to narrow results
   
4. **View Profile**: Click "Profile"
   - See your information
   - View recommended jobs

### For Administrators

1. **Login as Staff**: Use staff/admin credentials

2. **Frontend Admin Panel**: http://127.0.0.1:8000/admin_board/
   - View live statistics
   - Click "Add New Job" to create
   - Click "Edit" to modify existing jobs
   - Click "Delete" to remove jobs
   - Use search and filters

3. **Django Admin**: http://127.0.0.1:8000/admin/
   - Full Django admin interface
   - Manage jobs, users, and more
   - Changes sync to frontend instantly

## API Endpoints

All API endpoints return JSON:

- `GET /accounts/api/stats/` - Dashboard statistics (includes bookmarks and category breakdown)
- `GET /accounts/api/jobs/` - List all jobs (supports filters: `q`, `job_type`, `is_active`, `category`, `salary_min`, `salary_max`, pagination)
- `POST /accounts/api/jobs/` - Create new job
- `GET /accounts/api/jobs/<id>/` - Get job details
- `PUT /accounts/api/jobs/<id>/` - Update job
- `DELETE /accounts/api/jobs/<id>/` - Delete job
- `POST /accounts/api/jobs/<id>/apply/` - Apply to a job (auth required)
- `POST|DELETE /accounts/api/jobs/<id>/bookmark/` - Bookmark/unbookmark a job (auth required)
- `GET /accounts/api/bookmarks/` - List user bookmarks (auth required)
- `GET /accounts/api/applications/` - List user applications (auth required)
- `GET|PUT|PATCH /accounts/api/profile/` - Get/update profile (`bio`, `skills[]`)
- `POST /accounts/api/profile/resume/` - Upload resume file (multipart)
- `GET /accounts/api/notifications/` - List notifications
- `POST /accounts/api/notifications/<id>/read/` - Mark notification as read
- `POST /accounts/login/` - User login
- `POST /accounts/signup/` - User registration

## Database Schema

### Job Model
- title
- company_name
- location
- job_type (Full-time, Part-time, Contract, Internship)
- description
- requirements
- salary_min / salary_max
- is_active (boolean)
- posted_date (auto)
- experience_level (entry, mid, senior, lead)
- company_logo (URL)
- applications_count

## Project Structure

```
myproject/
├── manage.py
├── accounts/                    # Main app
│   ├── models.py               # Job, Category, Profile, Skills, Applications, Bookmarks, Notifications
│   ├── views.py                # API endpoints + auth
│   ├── urls.py                 # App routes
│   ├── admin.py                # Django admin config
│   └── management/
│       └── commands/
│           ├── seed_jobs.py    # Sample jobs seeder
│           └── seed_extra.py   # Categories, skills, sample profile/activity
├── myproject/                   # Project config
│   ├── settings.py
│   ├── urls.py                 # Main routes
│   └── views.py                # Page views
├── templates/                   # HTML templates
│   ├── index.html              # Homepage
│   ├── jobs.html               # Job listings
│   ├── login.html              # Login page
│   ├── signup.html             # Registration
│   ├── profile.html            # User profile
│   └── admin_board.html        # Admin dashboard
└── static/                      # Static files
    ├── css/
    │   ├── style.css
    │   ├── forms.css
    │   └── admin_board.css
    └── js/
        ├── auth.js             # Login/signup logic
        ├── admin_board.js      # Admin panel CRUD
        └── main.js             # General scripts
```

## Testing the Integration

1. **Add Job in Django Admin**:
   - Go to http://127.0.0.1:8000/admin/
   - Navigate to Jobs → Add Job
   - Fill in details and save

2. **Verify in Frontend Admin**:
   - Go to http://127.0.0.1:8000/admin_board/
   - Refresh the page
   - The new job appears in the table

3. **Verify on Jobs Page**:
   - Go to http://127.0.0.1:8000/jobs/
   - The job appears in the listing

## Admin Credentials

Default admin account:
- **Username**: admin
- **Password**: admin123

*Note: Change these credentials in production!*

## Troubleshooting

### Server won't start
- Ensure Python is installed and in PATH
- Check if port 8000 is available: `netstat -ano | findstr :8000`
- Try alternate port: `python manage.py runserver 8001`

### Jobs not showing
- Run: `python manage.py seed_jobs` to add sample data
- Check database: Jobs should appear in Django admin

### Can't login
- Verify user exists: `python manage.py createsuperuser`
- Check browser console for JavaScript errors
- Ensure CSRF token is present in forms

### Static files not loading
- Verify `STATIC_URL` in settings.py
- Check templates use `{% load static %}` and `{% static 'path' %}`

## Technologies Used

- **Backend**: Django 6.0.1, Python 3.12
- **Frontend**: Vanilla JavaScript, HTML5, CSS3
- **Database**: SQLite3 (development)
- **API**: RESTful JSON endpoints

## Future Enhancements

- [x] Job application system
- [x] User resume upload
- [x] Basic recommendations from profile skills
- [x] Bookmarks with listing page
- [x] Applications list page
- [ ] Email notifications
- [ ] Advanced search with Elasticsearch
- [ ] Company profiles

---

**License**: MIT
**Author**: Job Access Recommendation Team
**Version**: 1.0.0
