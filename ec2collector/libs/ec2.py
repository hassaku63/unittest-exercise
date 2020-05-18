import os
import json
import boto3
from botocore.exceptions import ClientError
from ec2collector.libs.kinesis import put_action_record
from ec2collector import settings

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def collect_ec2_instances_info():
    """
    実行しているリージョンに存在する EC2 すべてについて、タグを取得して返す機能

    ※今回の課題では、実際に EC2 API を呼び出すことはせず、タグ取得機能を模したダミー関数を提供します。
    時間内で余力があれば、こちらも実際に動くコードに直しつつテストの切り出しに挑戦してみてください。

    :return: List of dict {'InstanceId': <instance-id>, 'Tags': [<tags>]}
    :rtype: list
    """
    # ダミー実装
    import random
    letters = '0123456789abcdef'
    tag_coords = [
        {'Key': 'tag-key1', 'Value': 'value1'},
        {'Key': 'tag-key2', 'Value': 'value2'},
        {'Key': 'tag-key3', 'Value': 'value3'},
        {'Key': 'require_action', 'Value':'true'}
    ]
    result = []
    for i in range(5):
        tags = random.sample(tag_coords, k=2)
        result.append({
            'InstanceId': 'i-' + ''.join(random.choices(letters, k=17)),
            'Tags': tags
        })
    return result

    # 以下、参考実装
    # client = boto3.client('ec2', region_name=settings.AWS_REGION)
    # 
    # ret = client.describe_instances()
    # instances = []
    # try:
    #     for reservations in ret['Reservations']:
    #         for instance in reservations['Instances']:
    #             instances.append({
    #                 'InstanceId': instance['InstanceId'],
    #                 'Tags': instance['Tags']
    #             })
    # 
    # return ret