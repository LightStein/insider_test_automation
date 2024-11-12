FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the project files to the container
COPY ./selenium-project/ ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable to use headless mode
ENV HEADLESS=true

# Run the tests
CMD ["sh", "-c", "pytest --junitxml=report.xml && aws s3 cp report.xml s3://selenium-test-results-anri-giorganashvili/insider_test_results/"]