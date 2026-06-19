FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Upgrade pipeline toolchain inside container
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Install required runtime dependencies directly
RUN pip install --no-cache-dir flask google-cloud-aiplatform pydantic

# Copy the entire workspace into the container image context
COPY . .

EXPOSE 8080

CMD ["python", "main.py"]