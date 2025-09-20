# Use official Python 3.12.5 slim image
FROM python:3.12.5-slim

# Install system dependencies (PortAudio, ffmpeg, build tools)
RUN apt-get update && \
    apt-get install -y portaudio19-dev ffmpeg build-essential && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

# Make migrations and migrate database
RUN python manage.py makemigrations
RUN python manage.py migrate

# Expose the port
ENV PORT=10000
EXPOSE $PORT

# Start the app with Gunicorn + Uvicorn worker
CMD ["gunicorn", "ResumeService.asgi:application", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:$PORT"]
