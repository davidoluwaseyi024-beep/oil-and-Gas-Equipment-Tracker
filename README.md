# Equipment Tracker — Oil & Gas Asset Management

A Django web app to track equipment status, locations, and service schedules across facilities.

---

## Quick Start in PyCharm

### 1. Open the project
File → Open → select the `equipment_tracker_full` folder

### 2. Create a virtual environment
PyCharm will prompt you, or go to:
Settings → Project → Python Interpreter → Add → Virtualenv → Create

### 3. Install dependencies
Open the PyCharm terminal (bottom bar) and run:
```
pip install -r requirements.txt
```

### 4. Run migrations
```
python manage.py migrate
```

### 5. Create your admin user
```
python manage.py createsuperuser
```
Or use the pre-seeded account: **admin / admin123**

### 6. Run the development server
```
python manage.py runserver
```
Then open: http://127.0.0.1:8000

---

## Login
- URL: http://127.0.0.1:8000/login/
- Default credentials: `admin` / `admin123`

## Pages
| URL | Page |
|-----|------|
| / | Dashboard |
| /equipment/ | All Equipment (search + filter) |
| /overdue/ | Overdue Equipment |
| /equipment/add/ | Add New Equipment |
| /equipment/<pk>/ | Equipment Detail |
| /equipment/<pk>/edit/ | Edit Equipment |
| /admin/ | Django Admin Panel |

---

## Project Structure
```
equipment_tracker_full/
├── manage.py
├── requirements.txt
├── db.sqlite3              ← auto-created after migrate
├── equipment_tracker/
│   ├── settings.py
│   └── urls.py
├── tracker/
│   ├── models.py           ← Equipment model
│   ├── views.py            ← all function-based views
│   ├── urls.py             ← app URL patterns
│   ├── forms.py            ← ModelForm
│   ├── admin.py            ← admin registration
│   └── templates/
│       ├── registration/login.html
│       └── tracker/
│           ├── base.html
│           ├── dashboard.html
│           ├── equipment_list.html
│           ├── equipment_detail.html
│           ├── equipment_form.html
│           ├── equipment_confirm_delete.html
│           └── _status_badge.html
└── static/
    ├── css/main.css
    └── js/main.js
```

## Sample Data
8 equipment records are pre-seeded including overdue, critical, and upcoming service items so the dashboard is populated immediately.
