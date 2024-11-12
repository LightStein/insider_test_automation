#!/bin/bash

# Run additional setup commands if needed
chmod +x ./upload_to_s3.sh

# Run tests
if [ "$HEADLESS" = true ]; then
    pytest --headless tests/
else
    pytest tests/
fi

# Upload to S3 after tests
./upload_to_s3.sh
