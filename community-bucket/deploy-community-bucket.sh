#!/bin/bash
sam deploy --no-confirm-changeset --stack-name community-bucket \
--region us-east-2 --template-file community-bucket.yaml
