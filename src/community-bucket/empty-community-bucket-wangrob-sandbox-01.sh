#!/bin/bash
echo "Emptying community bucket in wangrob-sandbox-01."

aws s3 rm s3://community.octank-01.edu.rwang5688.com-867830616001 --recursive \
--profile wangrob-sandbox-01

echo "Done"
