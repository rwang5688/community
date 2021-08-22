from __future__ import print_function
import boto3
import os
from decimal import Decimal

rekognition = boto3.client('rekognition')

# Fall back for missing deployment parameters and OS environment variables
OFFENSIVE_LABELS = [
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

def is_offensive_label(mod_label, offensive_labels, mod_details):
    for offensive_label in offensive_labels:
        # report the first offensive label that exceeds confidence threshold
        if((mod_label['ParentName'] == offensive_label or mod_label['Name'] == offensive_label) and \
            Decimal(str(mod_label['Confidence'])) >= CONFIDENCE_THRESHOLD):
            error_message = "Image has " + offensive_label + " Content."
            mod_details['Pass'] = False
            mod_details['ErrorMessages'].append(error_message)
            return True
    
    return False

def detect_moderation_labels(bucket, key, input_params):
    # get environment variables
    env_var_name = 'OFFENSIVE_LABELS'
    default_value = OFFENSIVE_LABELS
    offensive_labels = get_env_var_list(env_var_name, default_value)
    print("offensive_labels=%s" % (offensive_labels))

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

    # stop after we find first label that may be offensive
    mod_labels = mod_response['ModerationLabels']
    for mod_label in mod_labels:
        if is_offensive_label(mod_label, offensive_labels, mod_details):
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

