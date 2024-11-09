FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the project files to the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable to use headless mode
ENV HEADLESS=true

# Run the tests
CMD ["pytest", "test_insider_careers.py"]