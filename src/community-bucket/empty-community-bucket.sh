#!/bin/bash
echo "Emptying community bucket in default."

aws s3 rm s3://community.octank-01.edu.rwang5688.com-867830616001 --recursive \
--profile default

echo "Done"
