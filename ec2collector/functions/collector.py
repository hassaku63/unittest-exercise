import json
import boto3
from boto3_type_annotations.dynamodb import Table
from ec2collector.libs.ec2 import collect_ec2_instances_info
from ec2collector import settings

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def get_table(TABLE_NAME):
    try:
        dynamo = boto3.resource('dynamodb')
        table: Table = dynamo.Table(TABLE_NAME)

        return table

    except Exception as e:
        log.error(e)
        raise e


def put_tag_info(table, instances):
    try:
        # boto3.resource().Table().batch_writer().__enter__.put_item()
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


def collect(event, context):
    """
    この Lambda が実行されているリージョンにある全ての EC2 をリストして、
    タグ情報を保存する機能
    """
    try:
        instances = collect_ec2_instances_info()
        dynamo = boto3.resource('dynamodb')
        table: Table = dynamo.Table(settings.TABLE_NAME)
        put_tag_info(table, instances)

        return instances

    except Exception as e:
        log.error(e)
        raise e


if __name__ == '__main__':
    # for test run in based on your local environemnt
    ret = collect({}, {})
    print(json.dumps(ret, indent=2))
