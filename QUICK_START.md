# Quick Reference Guide

## 🚀 Start the Server

```bash
cd "Job Access Recommendation System/myproject"
python manage.py runserver 0.0.0.0:8000
```

## 🌐 Important URLs

| Page | URL |
|------|-----|
| Homepage | http://127.0.0.1:8000/ |
| Jobs Listing | http://127.0.0.1:8000/jobs/ |
| Login | http://127.0.0.1:8000/login/ |
| Signup | http://127.0.0.1:8000/signup/ |
| Profile | http://127.0.0.1:8000/profile/ |
| Bookmarks | http://127.0.0.1:8000/bookmarks/ |
| Applications | http://127.0.0.1:8000/applications/ |
| Admin Dashboard | http://127.0.0.1:8000/admin_board/ |
| Django Admin | http://127.0.0.1:8000/admin/ |

## 👤 Login Credentials

**Admin Account**:
- Email: `admin@admin.com`
- Password: `admin123`

## 📋 Common Tasks

### Create New Admin User
```bash
python manage.py createsuperuser
```

### Apply Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Populate Demo Data
```bash
python seed_jobs.py
```

### Collect Static Files
```bash
python manage.py collectstatic
```

### Kill Server Process
```bash
taskkill /F /IM python.exe
```

## 🔍 Testing Workflow

1. **Test Signup**:
   - Go to /signup/
   - Create account with username, email, password
   - Should redirect to homepage

2. **Test Login**:
   - Go to /login/
   - Use email and password
   - Should redirect to homepage with username visible

3. **Test Job Search**:
   - Go to /jobs/
   - Enter keyword: "Python"
   - See filtered results

4. **Test Apply**:
   - Click "Apply" on any job
   - Should see success message
   - Check /applications/ to confirm

5. **Test Bookmark**:
   - Click "Bookmark" on any job
   - Check /bookmarks/ to confirm

6. **Test Profile**:
   - Go to /profile/
   - Click "Edit Bio" and update
   - Click "Add Skill" and select skills
   - Upload resume file
   - Add education and experience

## 📊 Database Info

- **Total Jobs**: 27 (seeded)
- **Categories**: 8
- **Skills**: 53
- **Database File**: `db.sqlite3`

## 🛠️ Troubleshooting

### Issue: "Port already in use"
```bash
taskkill /F /IM python.exe
python manage.py runserver 0.0.0.0:8000
```

### Issue: "CSRF verification failed"
- Clear browser cookies
- Refresh the page
- Check CSRF token in form

### Issue: "Static files not loading"
- Verify server is running
- Check browser console for 404 errors
- Ensure `{% load static %}` is in template

### Issue: "Apply button not working"
- Make sure you're logged in
- Check browser console for errors
- Verify CSRF token is being sent

## 📱 Features Checklist

- [x] User Signup/Login
- [x] Job Search & Filter
- [x] Apply to Jobs
- [x] Bookmark Jobs
- [x] Profile Management
- [x] Education Tracking
- [x] Experience Tracking
- [x] Resume Upload
- [x] Skills Management
- [x] Notifications
- [x] Admin Dashboard
- [x] Job Recommendations
- [x] Activity Logging

## 🎯 Quick Testing Commands

```bash
# Start server
python manage.py runserver 0.0.0.0:8000

# Check migrations
python manage.py showmigrations

# Access Django shell
python manage.py shell

# Create test user
python manage.py createsuperuser --username testuser --email test@test.com
```

## 📞 Need Help?

- Check `TESTING_GUIDE.md` for detailed testing procedures
- Check `README.md` for full documentation
- Review browser console (F12) for JavaScript errors
- Check terminal for Django errors

---

**Quick Tip**: Keep this file open while testing the application!
