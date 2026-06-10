# Dockerfile for Render deployment
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create staticfiles directory
RUN mkdir -p /app/staticfiles

# Collect static files, skip errors if any
RUN python manage.py collectstatic --noinput --ignore=*.woff --ignore=*.woff2 --ignore=*.ttf 2>&1 || true

EXPOSE 10000

CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py collectstatic --noinput 2>&1 || true && gunicorn myproject.wsgi:application --bind 0.0.0.0:$PORT --workers 3"]
