# Dockerfile for Containerizing the Test Project
# Create a Docker image for the test project
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the project files
COPY . /app

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Run the tests
CMD ["pytest", "./app/test_insider_careers.py"]
