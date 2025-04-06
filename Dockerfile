# Use a slim Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (optional but helpful)
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
