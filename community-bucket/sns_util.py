from __future__ import print_function
import boto3
import json
import os

sns = boto3.client('sns')

# Fall back for missing deployment parameters and OS environment variables
ROOT_URL =  'https://mycommunity.octank.edu.rwang5688.com/'
TOPIC_ARN = 'arn:aws:sns:us-east-1:375205257662:mycommunity-octank-edu-detect-moderation-labels'

def get_env_var(env_var_name, default_value):
    env_var = os.environ[env_var_name]
    if env_var == '':
        print("WARNING: Cannot get environment variable %s.  Fall back to hard coded const." % (env_var_name))
        env_var =  default_value

    return env_var    

def send_moderation_warning(key, input_params):
    # get environment variables
    env_var_name = 'ROOT_URL'
    default_value = ROOT_URL
    root_url = get_env_var(env_var_name, default_value)
    print("root_url=%s" % (root_url))

    env_var_name = 'TOPIC_ARN'
    default_value = TOPIC_ARN
    topic_arn = get_env_var(env_var_name, default_value)
    print("topic_arn=%s" % (topic_arn))

    # get moderation result components for subject line and message body
    mod_result = input_params['ModerationResult']
    mod_errors = mod_result['Details']['ErrorMessages']
    mod_labels = mod_result['Labels']

    # compose subject line
    subject = "WARNING: " + mod_errors[0]
    print("Subject=%s" % (subject))

    # compose message body
    message = "Image file: " + root_url + key + "\n"
    message = message + "\nError Messages:\n" + \
        "===\n"
    for mod_error in mod_errors:
        message = message + \
            "Error Message: " + mod_error + "\n" + \
            "===\n"
    message = message + "\nModeration Labels:\n" + \
        "===\n"
    for mod_label in mod_labels:
        parent_label = mod_label['ParentName']
        if parent_label == '':
            message = message + \
                "Label: " + mod_label['Name'] + "\n" + \
                "Confidence: " + str(mod_label['Confidence']) + "\n" + \
                "===\n"
        else:
            message = message + \
                "   Parent Label: " + mod_label['ParentName'] + "\n" + \
                "   Label: " + mod_label['Name'] + "\n" + \
                "   Confidence: " + str(mod_label['Confidence']) + "\n" + \
                "===\n"
    print("Message=%s" % (message))
    
    pub_response = sns.publish(
        TargetArn=topic_arn,
        Subject=subject,
        Message=json.dumps({'default': message}),
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

