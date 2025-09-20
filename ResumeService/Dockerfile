FROM python:3.12

# Set working directory
WORKDIR /app

# Install system dependencies for building Python packages and multimedia processing
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    ffmpeg \
    libpq-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and upgrade pip
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip setuptools wheel

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy project code
COPY . .

# Django migrations
RUN python manage.py makemigrations
RUN python manage.py migrate

# Expose port
EXPOSE 8000

# Run server with Gunicorn + Uvicorn
CMD ["gunicorn", "ResumeService.asgi:application", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
