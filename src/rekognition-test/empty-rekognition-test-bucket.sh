#!/bin/bash
echo "Emptying community bucket in default."

aws s3 rm s3://rekognition-test-data-bucket --recursive \
--profile default

echo "Done"
