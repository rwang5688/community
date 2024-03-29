#!/bin/bash
echo "Deploy community-bucket stack (including publishContent function) in default."

sam deploy --guided --stack-name community-bucket \
--template-file community-bucket.yaml \
--profile default \
--region us-east-1

echo "Done"
