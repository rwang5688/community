#!/bin/bash
echo "Deploy community-bucket stack (including publishContent function) in wangrob-sandbox-01."

sam deploy --guided --stack-name community-bucket \
--template-file community-bucket.yaml \
--profile wangrob-sandbox-01 \
--region us-east-1

echo "Done"
