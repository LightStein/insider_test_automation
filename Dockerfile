FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy necessary files
COPY ./selenium-project/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY ./selenium-project/ ./

# Set environment variables
ENV HEADLESS=true
ENV PYTHONUNBUFFERED=1

# Add an entrypoint script
COPY ./selenium-project/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Run entrypoint script
ENTRYPOINT ["/app/entrypoint.sh"]
