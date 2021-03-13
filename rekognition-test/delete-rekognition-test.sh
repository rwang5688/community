#!/bin/bash
aws s3 rm s3://rekognition-test-data-bucket --recursive
aws cloudformation delete-stack --stack-name rekognition-test
