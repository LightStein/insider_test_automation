FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the project files to the container
COPY ./selenium-project/ ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install AWS CLI
RUN apt-get update && apt-get install -y awscli && apt-get clean

# Set environment variable to use headless mode
ENV HEADLESS=true

# Run the tests and upload results to S3
CMD ["sh", "-c", "pytest test_insider_careers.py > test_output.txt; aws s3 cp test_output.txt s3://selenium-test-results-anri-giorganashvili/insider_test_results"]
