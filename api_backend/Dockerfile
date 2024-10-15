# Use official Python image as base
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project
COPY . /app/

# Collect static files (optional, since no data storage)
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run migrations (optional, since no data storage)
# RUN python manage.py migrate

# Define the default command
CMD ["gunicorn", "api_backend.wsgi:application", "--bind", "0.0.0.0:8000"]
