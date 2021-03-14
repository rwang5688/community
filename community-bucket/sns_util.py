from __future__ import print_function
import boto3
import json
import os

sns = boto3.client('sns')

TOPIC_ARN = 'arn:aws:sns:us-east-2:375205257662:community-octank-edu-detect-moderation-labels'

def send_moderation_warning(bucket, key, input_params):
    mod_result = input_params['ModerationResult']
    mod_errors = mod_result['Details']['ErrorMessages']

    topic_arn = os.environ['TOPIC_ARN']
    if topic_arn == '':
        print("WARNING: Cannot TOPIC_ARN get environment variable.  Fall back to hard coded const.")
        topic_arn =  TOPIC_ARN
    print("TopicArn=%s" % (topic_arn))

    subject = "WARNING: " + json.dumps(mod_errors)
    message = {
        'Bucket': bucket,
        'Image': key,
        'ModerationResult': mod_result
    }
    print("Subject=%s" % (subject))
    print("Message=%s" % (json.dumps(message)))
    
    pub_response = sns.publish(
        TargetArn=topic_arn,
        Subject=subject,
        Message=json.dumps({'default': json.dumps(message)}),
        MessageStructure='json'
    )

    pub_result = {
        'Response': pub_response,
        'TopicArn': topic_arn,
        'Subject': subject,
        'Message': message
    }

    input_params['PublishMessageResult'] = pub_result
    return input_params

