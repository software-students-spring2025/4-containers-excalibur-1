# Use a Python base image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Install system dependencies (required by OpenCV, moviepy, etc.)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file and install Python packages
COPY requirement.txt .
RUN pip install --upgrade pip
RUN pip install -r requirement.txt

# Copy the rest of the ML client code
COPY . .

# Default command to run your script
CMD ["python", "app.py"]
