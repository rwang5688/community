#!/bin/bash
sam deploy --guided --stack-name community-bucket \
--region us-east-1 --template-file community-bucket.yaml
