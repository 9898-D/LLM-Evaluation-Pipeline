# Use official Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app/

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose ports for Django
EXPOSE 8000

# Run both Django and Celery in the same container
CMD ["sh", "-c", "python manage.py migrate && \
                   python manage.py runserver 0.0.0.0:8000 & \
                   celery -A evaluation worker --loglevel=info"]
