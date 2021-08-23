#!/bin/bash
echo "Deploy rekognition-test test (including rekognitionTest function) in wangrob-sandbox-01."

sam deploy --guided --stack-name rekognition-test \
--template-file rekognition-test.yaml \
--profile wangrob-sandbox-01 \
--region us-east-1

echo "Done"
