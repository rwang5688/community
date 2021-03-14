from __future__ import print_function
import boto3
from decimal import Decimal

rekognition = boto3.client('rekognition')

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
        if((mod_label['ParentName'] == 'Violence' or mod_label['Name'] == 'Violence') and Decimal(str(mod_label['Confidence'])) >= 70):
            # print('Image has Violence Content.')
            mod_details['Pass'] = False
            mod_details['ErrorMessages'].append('Image has Violence Content.')
            break

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

