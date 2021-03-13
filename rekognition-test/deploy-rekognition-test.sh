#!/bin/bash
sam deploy --stack-name rekognition-test --no-confirm-changeset \
--template-file rekognition-test.yaml
