# Use official Python image from DockerHub
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && pip install psycopg2-binary

# Copy app file into container
COPY . .

# Tell Docker how to run it
CMD ["python3", "app.py"]


# RUN pip install psycopg2-binary