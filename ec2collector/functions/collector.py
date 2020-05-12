import os
import json
from datetime import datetime
import boto3
from ec2collector import settings

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def get_instances():
    """実行リージョンの
    """
    pass


def handler(event, context):
    client = boto3.client('ec2', region_name=settings.AWS_REGION)

    ret = client.describe_instances()
    instances = []
    try:
        for reservations in ret['Reservations']:
            for instance in reservations['Instances']:
                instances.append({
                    'InstanceId': instance['InstanceId'],
                    'Tags': instance['Tags']
                })

    except Exception as e:
        log.error(e)
        raise e


if __name__ == '__main__':
    # for test run in based on your local environemnt
    ret = handler({}, {})
    print(ret)

