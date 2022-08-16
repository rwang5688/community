#!/bin/bash
echo "Emptying community bucket in default."

aws s3 rm s3://community-123456789012-us-west-2 --recursive \
--profile default

echo "Done"
