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

## Render Deployment
1. Push this repository to GitHub or connect your Git provider to Render.
2. In Render, create a new Web Service with environment `Docker`.
3. Use the repository root and `Dockerfile` from this repo.
4. Set required environment variables in Render:
   - `DJANGO_DEBUG=False`
   - `DJANGO_SECRET_KEY=<secure-secret>`
   - `DJANGO_ALLOWED_HOSTS=<your-render-service>.onrender.com`
5. Render will build the container, run `collectstatic`, and start the app with Gunicorn.

If you make static file changes, re-deploy the Render service so collectstatic runs again.
