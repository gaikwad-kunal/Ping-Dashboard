# Use a lightweight version of Python
FROM python:3.9-slim

# Install the system ping utility required by the OS inside the container
RUN apt-get update && apt-get install -y iputils-ping && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy your files into the container
COPY requirements.txt .
COPY app.py .

# Install Flask
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
