#!/bin/bash
echo "Delete community-bucket stack (including publishContent function) from default."

aws cloudformation delete-stack --stack-name community-bucket \
--profile default \
--region us-east-1

echo "Done"
