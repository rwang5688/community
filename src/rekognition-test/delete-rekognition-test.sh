#!/bin/bash
echo "Delete rekognition-test stack (including rekognitionTest function) from default."

aws cloudformation delete-stack --stack-name rekognition-test \
--profile default \
--region us-east-1

echo "Done"
