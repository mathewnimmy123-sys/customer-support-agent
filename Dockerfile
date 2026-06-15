# Use an official, lightweight Python runtime as the base image
FROM python:3.11-slim

# Prevent Python from writing pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# Copy dependency definitions and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code (main.py, support_agent, config)
COPY . .

# Expose port 8080 (the default standard for GCP Cloud Run workloads)
EXPOSE 8080

# The command to execute when the container starts up
CMD ["python", "main.py"]