# Job Recommendation System

A Django-based web application that provides AI-powered job recommendations for job seekers and an admin dashboard to manage job listings and users.

## Features

- **User Management**: Registration, login, and profile management with JWT authentication
- **User Profiles**: Resume upload, skills tracking, education, and experience details
- **Job Listings**: CRUD operations for job postings (admin-only)
- **AI Recommendations**: TF-IDF based text similarity between user profiles and job descriptions
- **REST API**: Complete RESTful API built with Django REST Framework
- **Admin Dashboard**: Django admin interface for managing users and jobs

## Technology Stack

- **Backend**: Django 4.2+
- **API**: Django REST Framework
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Machine Learning**: scikit-learn (TF-IDF vectorization)
- **Database**: SQLite (development), easily configurable for PostgreSQL/MySQL
- **Resume Parsing**: PyPDF2

## Project Structure

```
job-rec-system/
├── access_rec/          # Main project directory
│   ├── settings.py      # Project settings
│   ├── urls.py          # Main URL configuration
│   └── wsgi.py          # WSGI application
├── accounts/            # User accounts app
│   ├── models.py        # UserProfile model
│   ├── views.py         # Authentication and profile views
│   ├── serializers.py   # User and profile serializers
│   └── urls.py          # Account-related URLs
├── jobs/                # Job listings app
│   ├── models.py        # Job model
│   ├── views.py         # Job CRUD and recommendation views
│   ├── serializers.py   # Job serializers
│   ├── recommender.py   # ML recommendation engine
│   └── urls.py          # Job-related URLs
├── manage.py            # Django management script
└── requirements.txt     # Python dependencies

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/mirzaabdullaht/job-rec-system.git
   cd job-rec-system
   ```

2. **Create and activate a virtual environment**:
   
   **On Windows (PowerShell)**:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   
   **On macOS/Linux**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables** (optional):
   Create a `.env` file in the root directory:
   ```
   DJANGO_SECRET_KEY=your-secret-key-here
   DJANGO_DEBUG=1
   ```

5. **Apply database migrations**:
   ```bash
   python manage.py migrate
   ```

6. **Create a superuser** (for admin access):
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

8. **Access the application**:
   - API: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

## API Endpoints

### Authentication
- `POST /api/accounts/register/` - Register a new user
- `POST /api/accounts/login/` - Login and get JWT tokens
- `POST /api/accounts/token/refresh/` - Refresh access token
- `POST /api/accounts/logout/` - Logout (blacklist token)

### User Profile
- `GET /api/accounts/profile/` - Get current user's profile
- `PUT /api/accounts/profile/` - Update current user's profile
- `PATCH /api/accounts/profile/` - Partial update of profile

### Jobs
- `GET /api/jobs/` - List all active jobs
- `POST /api/jobs/` - Create a new job (authenticated users)
- `GET /api/jobs/{id}/` - Get job details
- `PUT /api/jobs/{id}/` - Update job (admin only)
- `DELETE /api/jobs/{id}/` - Delete job (admin only)
- `GET /api/jobs/recommendations/` - Get personalized job recommendations

## Usage Examples

### Register a new user
```bash
curl -X POST http://127.0.0.1:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepass123",
    "password_confirm": "securepass123",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Login
```bash
curl -X POST http://127.0.0.1:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "password": "securepass123"
  }'
```

### Update profile
```bash
curl -X PATCH http://127.0.0.1:8000/api/accounts/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "skills": "Python, Django, Machine Learning, REST API",
    "education": "BS Computer Science, University XYZ",
    "experience": "3 years as Backend Developer at Company ABC"
  }'
```

### Get job recommendations
```bash
curl -X GET http://127.0.0.1:8000/api/jobs/recommendations/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## How the Recommendation System Works

The recommendation engine uses **TF-IDF (Term Frequency-Inverse Document Frequency)** vectorization to find jobs that match a user's profile:

1. User profile text is created from: skills + education + experience
2. Job descriptions are collected from active job listings
3. TF-IDF vectorizer converts all texts into numerical vectors
4. Cosine similarity is calculated between the user's profile and each job
5. Top N jobs with highest similarity scores are returned

This is a simple but effective approach for a prototype. For production, consider:
- More sophisticated NLP techniques (word embeddings, BERT)
- User behavior tracking and collaborative filtering
- A/B testing for recommendation quality
- Caching and background processing for performance

## Development Notes

- This is a **prototype/MVP** focused on architecture and core functionality
- For production deployment:
  - Use a production-grade database (PostgreSQL, MySQL)
  - Set `DEBUG=False` and configure proper `ALLOWED_HOSTS`
  - Use environment variables for secrets
  - Enable HTTPS
  - Add rate limiting and security middleware
  - Implement proper resume parsing (PyPDF2 is basic)
  - Add comprehensive logging and monitoring
  - Consider background task processing (Celery)

## Testing

Run tests with:
```bash
python manage.py test
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Contact

For questions or support, please open an issue on GitHub.
