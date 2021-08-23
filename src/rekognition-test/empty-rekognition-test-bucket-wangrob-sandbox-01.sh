#!/bin/bash
echo "Emptying community bucket in wangrob-sandbox-01."

aws s3 rm s3://rekognition-test-data-bucket --recursive \
--profile wangrob-sandbox-01

echo "Done"
