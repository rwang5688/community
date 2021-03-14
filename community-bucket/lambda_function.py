from __future__ import print_function
import json
import urllib
import pathlib 

import cloudfront_util
import rekognition_util
import sns_util


def lambda_handler(event, context):

    print("Received event: %s." % (json.dumps(event, indent=2)))

    # Create invalidation
    event = cloudfront_util.create_invalidation(event)
    print("After create invalidation: %s." % (json.dumps(event, indent=2)))

    # Get the object from the event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])

    # Check if the object is an image
    file_extension = pathlib.Path(key).suffix 
    print("File Extension: ", file_extension)
    if ((file_extension != '.jpg') and (file_extension != '.png')):
        print("File %s is not an image. Skip moderation: %s." % (key, json.dumps(event, indent=2)))
        return event

    try:
        # Calls rekognition DetectModerationLabels API to detect faces in S3 object
        response = rekognition_util.detect_moderation_labels(bucket, key, event)

        # Print moderation result to console.
        mod_result = response['ModerationResult']
        print("Moderation result: %s." % (mod_result))

        # If image failed moderation, send moderation warning
        mod_pass = mod_result['Pass']
        if mod_pass is False:
            response = sns_util.send_moderation_warning(bucket, key, response)
        
        print("After moderation: %s." % (json.dumps(response, indent=2)))
        return response
    except Exception as e:
        print(e)
        print("Error processing object {} from bucket {}. ".format(key, bucket) +
              "Make sure your object and bucket exist and your bucket is in the same region as this function.")
        raise e

