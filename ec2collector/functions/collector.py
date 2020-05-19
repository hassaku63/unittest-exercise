import json
import boto3
from boto3_type_annotations.dynamodb import Table
from botocore.exceptions import ClientError
from ec2collector.libs.ec2 import collect_ec2_instances_info
from ec2collector.libs.kinesis import put_action_record
from ec2collector import settings

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def collect(event, context):
    """
    この Lambda が実行されているリージョンにある全ての EC2 をリストして、
    タグ情報を保存する機能
    """
    try:
        instances = collect_ec2_instances_info()
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
            if tag['Key'] == 'require_action' and tag['Value'] == 'true':
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

