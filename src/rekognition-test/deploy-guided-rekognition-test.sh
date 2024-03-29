#!/bin/bash
echo "Deploy rekognition-test test (including rekognitionTest function) in default."

sam deploy --guided --stack-name rekognition-test \
--template-file rekognition-test.yaml \
--profile default \
--region us-east-1

echo "Done"
