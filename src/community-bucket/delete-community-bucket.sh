#!/bin/bash
echo "Delete community-bucket stack (including publishContent function) from default."

aws cloudformation delete-stack --stack-name community-bucket \
--profile default

echo "Done"
