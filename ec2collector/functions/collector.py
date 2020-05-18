import os
import json
from datetime import datetime
from boto3_type_annotations.dynamodb import Table
import boto3
from botocore.exceptions import ClientError
from ec2collector.libs.kinesis import put_action_record
from ec2collector import settings

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def collect_instances_info():
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


def collect(event, context):
    """
    この Lambda が実行されているリージョンにある全ての EC2 をリストして、
    タグ情報を保存する機能
    """
    try:
        instances = collect_instances_info()
    except Exception as e:
        log.error(e)
        raise e

    try:
        dynamo = boto3.resource('dynamodb')
        table: Table = dynamo.Table(settings.TABLE_NAME)
        with table.batch_writer(overwrite_by_pkeys=['InstanceId']) as batch:
            # 参考: https://dev.classmethod.jp/articles/lambda-python-dynamodb/
            for instance in instances:
                batch.put_item(Item={
                    'InstanceId': instance['InstanceId'],
                    'Tags': instance['Tags']
                })
    except Exception as e:
        log.error(e)    
        raise e
    
    return instances


def something_action(event, context):
    """
    require_action == true のタグを持つインスタンスに対して、 something_action を実行する機能
    """
    items = []
    # Task1 - 収集したすべてのインスタンスタグ情報をScan
    try:
        dynamo = boto3.resource('dynamodb')
        table: Table = dynamo.Table(settings.TABLE_NAME)
        response = table.scan()
        items = response['Items']
    except ClientError as e:
        log.error(e.response['Error']['Message'])
        raise e

    # Task2 - 'require_action' タグを持つインスタンスにのみ何らかのアクションを実行する
    result = []
    for item in items:
        # tag_keys = [tag['Key'] for tag in item['Tags']]
        for tag in item['Tags']:
            if tag['Key'] == 'require_action':
                log.info(f"found required action: {item['InstanceId']}")
                result.append(item)
                break
    for instance in result:
        # do something action
        put_action_record(instance)

    return result


if __name__ == '__main__':
    # for test run in based on your local environemnt
    ret = collect({}, {})
    print(json.dumps(ret, indent=2))

