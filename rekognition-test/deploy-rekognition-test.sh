#!/bin/bash
sam deploy --no-confirm-changeset --stack-name rekognition-test \
--template-file rekognition-test.yaml
