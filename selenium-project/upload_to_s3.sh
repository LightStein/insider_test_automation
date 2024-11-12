#!/bin/bash
# upload_to_s3.sh

# Assuming test_output.txt is the report file
aws s3 cp test_output.txt s3://selenium-test-results-anri-giorganashvili/insider_test_results
