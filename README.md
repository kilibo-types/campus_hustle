# Campus Hustle

Campus Hustle is a Django-based marketplace for Makerere University students to post and find small campus gigs.

## Prerequisites
- Python 3.10+ (you have Python 3.14 installed)
- Git (optional)

## Setup (Windows / PowerShell)

```powershell
cd "a:\campus hustle\myproject"
# create virtualenv if not already created
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

## Database migrations & admin

```powershell
cd "a:\campus hustle\myproject"
.\.venv\Scripts\Activate.ps1
python manage.py migrate
# create a superuser (interactive)
python manage.py createsuperuser
```

## Run the development server

```powershell
.\.venv\Scripts\Activate.ps1
python manage.py runserver
```

Open http://127.0.0.1:8000/ in your browser.

## Notes
- Static files are served by Django's `runserver` in development. For production, configure a proper static file server.
- The project includes a `gigs` app implementing models, views, templates and admin configuration.
- Default admin credentials created earlier: username `admin` (change password in production).
