from __future__ import print_function
import boto3
import os
from decimal import Decimal

rekognition = boto3.client('rekognition')

# Fall back for missing deployment parameters and OS environment variables
LABEL_TYPES = [
    'Explicit Nudity',
    'Gambling',
    'Suggestive',
    'Violence'
]
CONFIDENCE_THRESHOLD = 67

def get_env_var_list(env_var_name, default_value):
    env_var = os.environ[env_var_name]
    if env_var == '':
        print("WARNING: Cannot get environment variable %s.  Fall back to hard coded const." % (env_var_name))
        delimiter = ","
        env_var =  delimiter.join(default_value)
    
    env_var_list = []
    env_var_split_list = env_var.split(",")
    for s in env_var_split_list:
        env_var_list.append(s.strip())
    return env_var_list

def get_env_var_float(env_var_name, default_value):
    env_var = os.environ[env_var_name]
    if env_var == '':
        print("WARNING: Cannot get environment variable %s.  Fall back to hard coded const." % (env_var_name))
        env_var =  str(default_value)

    env_var_float = float(env_var)
    return env_var_float

def check_label_type(mod_label, label_type, mod_details):
    # label type exists and confidence level exceed threshold
    if((mod_label['ParentName'] == label_type or mod_label['Name'] == label_type) and \
        Decimal(str(mod_label['Confidence'])) >= CONFIDENCE_THRESHOLD):
        error_message = "Image has " + label_type + " Content."
        mod_details['Pass'] = False
        mod_details['ErrorMessages'].append(error_message)
        return True
    
    return False

def detect_moderation_labels(bucket, key, input_params):
    # get environment variables
    env_var_name = 'LABEL_TYPES'
    default_value = LABEL_TYPES
    label_types = get_env_var_list(env_var_name, default_value)
    print("label_types=%s" % (label_types))

    env_var_name = 'CONFIDENCE_THRESHOLD'
    default_value = CONFIDENCE_THRESHOLD
    confidence_threshold = get_env_var_float(env_var_name, default_value)
    print("confidence_threshold=%f" % (confidence_threshold))

    mod_details = {
        'Stage' : 'DetectModerationLabels',
        'Pass': True,
        'ErrorMessages': []
    }
    
    mod_response = rekognition.detect_moderation_labels(
        Image={"S3Object": {"Bucket": bucket, "Name": key}}, MinConfidence=10)

    # stop after we find first label that fails moderation check
    mod_labels = mod_response['ModerationLabels']
    for mod_label in mod_labels:
        found_failed_label = False
        for label_type in label_types:
            if check_label_type(mod_label, label_type, mod_details):
                found_failed_label = True
                break
        if found_failed_label is True:
            break

    mod_result = {
        'Labels': mod_labels,
        'Details': mod_details,
        'Pass': mod_details['Pass']
    }
    if (mod_details['Pass'] is False):
        mod_result['Reason'] = 'IMAGE_MODERATION_APPLIED'
    else:
        mod_result['Reason'] = ''

    input_params['ModerationResult'] = mod_result
    return input_params

