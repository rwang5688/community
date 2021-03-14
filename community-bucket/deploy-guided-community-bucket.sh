#!/bin/bash
sam deploy --guided --stack-name community-bucket \
--region us-east-2 --template-file community-bucket.yaml
