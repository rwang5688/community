#!/bin/bash
echo "Delete rekognition-test stack (including rekognitionTest function) from wangrob-sandbox-01."

aws cloudformation delete-stack --stack-name rekognition-test \
--profile wangrob-sandbox-01 \
--region us-east-1

echo "Done"
