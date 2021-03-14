from __future__ import print_function
import boto3
import time
import os

client = boto3.client('cloudfront')

def create_invalidation(input_params):
    paths = []
    for items in input_params["Records"]:
        key = items["s3"]["object"]["key"]
        if key.endswith("index.html"):
            paths.append("/" + key[:-10] + "*")
        else:
            paths.append("/" + key)
    print("Invalidating: %s." % (str(paths)))

    distribution_id = os.environ['DISTRIBUTION_ID']
    batch = {
        'Paths': {
            'Quantity': len(paths),
            'Items': paths
        },
        'CallerReference': str(time.time_ns() // 1000000)
    }
    print("Calling create_invalidation with distribution_id=%s, batch=%s" % (distribution_id, batch))

    if distribution_id == "":
        print("Distribution Id is empty.  Skip create invalidation for now.")
        return input_params

    inv_response = client.create_invalidation(
        DistributionId=distribution_id,
        InvalidationBatch=batch,
    )
    print("Create invalidation response: %s." % (inv_response))

    inv_result = {
        'DistributionId': distribution_id,
        'Batch': batch
    }

    input_params['InvalidationResult'] = inv_result
    return input_params

