# Use official Python image from DockerHub
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    netcat-openbsd \
    && pip install psycopg2-binary

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# Copy app file into container
COPY . .

# 2) Replace CMD with a small wait‑then‑run script
CMD [ "sh", "-c", "\
      echo \"🕐 Waiting for Postgres at db:5432…\"; \
      until nc -z db 5432; do \
        echo \"…still waiting\"; \
        sleep 1; \
      done; \
      echo \"✅ Postgres is up — starting app…\"; \
      python3 app.py \
    " ]