
# # -------- BUILD STAGE --------
# FROM python:3.12-slim AS builder

# WORKDIR /app

# # Prevent cache & pyc
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# RUN apt-get update && apt-get install -y --no-install-recommends \
#     build-essential \
#     gcc \
#     && rm -rf /var/lib/apt/lists/*

# COPY requirements.txt .

# RUN pip install --upgrade pip \
#     && pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt

# # -------- RUNTIME STAGE --------
# FROM python:3.12-slim

# WORKDIR /app

# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1
# ENV DEEPFACE_HOME=/app/Components/deepfaceData

# COPY --from=builder /wheels /wheels

# RUN pip install --no-cache-dir /wheels/* \
#     && rm -rf /wheels

# COPY . .

# CMD ["python", "main.py"]

# -------- BUILD STAGE --------
FROM python:3.12-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip wheel --no-cache-dir --wheel-dir /wheels -r requirements.txt


# -------- RUNTIME STAGE --------
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEEPFACE_HOME=/app/Components/deepfaceData

# REQUIRED FOR OPENCV / CV2
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /wheels /wheels

RUN pip install --no-cache-dir /wheels/* \
    && rm -rf /wheels

COPY . .

CMD ["python", "main.py"]
