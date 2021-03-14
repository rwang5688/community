from __future__ import print_function

import boto3
from decimal import Decimal
import json
import urllib
import pathlib 

print('Loading function')

rekognition = boto3.client('rekognition')
sns = boto3.client('sns')

TOPIC_ARN = 'arn:aws:sns:us-east-2:375205257662:community-octank-edu-detect-moderation-labels'


# --------------- Helper Functions to call Rekognition APIs ------------------


def detect_moderation_labels(bucket, key, input_params):
    mod_details = {
        'Stage' : 'DetectModerationLabels',
        'Pass': True,
        'ErrorMessages': []
    }
    mod_response = rekognition.detect_moderation_labels(
        Image={"S3Object": {"Bucket": bucket, "Name": key}}, MinConfidence=10)
    for mod_label in mod_response['ModerationLabels']:
        if((mod_label['ParentName'] == 'Explicit Nudity' or mod_label['Name'] == 'Explicit Nudity') and Decimal(str(mod_label['Confidence'])) >= 70):
            # print('Image has Explicit Content.')
            mod_details['Pass'] = False
            mod_details['ErrorMessages'].append('Image has Explicit Content.')
            break
        if((mod_label['ParentName'] == 'Suggestive' or mod_label['Name'] == 'Suggestive') and Decimal(str(mod_label['Confidence'])) >= 70):
            # print('Image has Suggestive Content.')
            mod_details['Pass'] = False
            mod_details['ErrorMessages'].append('Image has Suggestive Content.')
            break

    # process overall result
    mod_result = {
        'Response': mod_response,
        'Details': mod_details,
        'Pass': mod_details['Pass']
    }
    if (mod_details['Pass'] is False):
        mod_result['Reason'] = 'IMAGE_MODERATION_APPLIED'
    else:
        mod_result['Reason'] = ''

    input_params['ModerationResult'] = mod_result
    return input_params


# --------------- Send moderation warning ------------------


def send_moderation_warning(bucket, key, response):
    mod_result = response['ModerationResult']
    mod_errors = mod_result['Details']['ErrorMessages']

    subject = "WARNING: " + json.dumps(mod_errors)
    message = {
        'Bucket': bucket,
        'Image': key,
        'ModerationResult': mod_result
    }

    print("Subject=%s" % (subject))
    print("Message=%s" % (json.dumps(message)))
    
    sns_response = sns.publish(
        TargetArn=TOPIC_ARN,
        Subject=subject,
        Message=json.dumps({'default': json.dumps(message)}),
        MessageStructure='json'
    )

    print('SNS response: %s.' % (sns_response))
    return sns_response


# --------------- Main handler ------------------


def lambda_handler(event, context):

    print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event
    #bucket = event['Params']['Bucket']
    #key = urllib.unquote_plus(event['Params']['Key'].encode('utf8'))
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])

    # function to return the file extension
    file_extension = pathlib.Path(key).suffix 
    print("File Extension: ", file_extension)
    if ((file_extension != '.jpg') and (file_extension != '.png')):
        print("File %s is not an image.  Skip moderation for now." % (key))
        return event

    try:
        # Calls rekognition DetectModerationLabels API to detect faces in S3 object
        response = detect_moderation_labels(bucket, key, event)

        # Print moderation result to console.
        mod_result = response['ModerationResult']
        print("Moderation result: %s." % (mod_result))

        # If image failed moderation, send moderation warning
        mod_pass = mod_result['Pass']
        if mod_pass is False:
            send_moderation_warning(bucket, key, response)

        return response
    except Exception as e:
        print(e)
        print("Error processing object {} from bucket {}. ".format(key, bucket) +
              "Make sure your object and bucket exist and your bucket is in the same region as this function.")
        raise e

