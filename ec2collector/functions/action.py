import boto3
import logging

from boto3_type_annotations.dynamodb import Table
from botocore.exceptions import ClientError
from ec2collector.libs.kinesis import put_action_record

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def scan_table(table):
    try:
        response = table.scan()
        items = response['Items']

        return items

    except ClientError as e:
        log.error(e.response['Error']['Message'])
        raise e


def extract_instance(items):
    try:
        result = []
        flag_element = {"Key": 'require_action', "Value": 'true'}
        for item in items:
            # tag_keys = [tag['Key'] for tag in item['Tags']]
            if flag_element in item["Tags"]:
                log.info(f"found required action: {item['InstanceId']}")
                result.append(item)

        return result

    except Exception as e:
        log.error(e)
        raise e


def something_action(event, context):
    """
    require_action == true のタグを持つインスタンスに対して、 something_action を実行する機能
    """
    items = []
    try:
        # Task1 - 収集したすべてのインスタンスタグ情報をScan
        dynamo = boto3.resource('dynamodb')
        table: Table = dynamo.Table(settings.TABLE_NAME)
        items = scan_table(table)

        # Task2 - 'require_action' タグを持つインスタンスにのみ何らかのアクションを実行する
        instances = extract_instance(items)
        list(map(lambda instance: put_action_record(instance), instances))

        return instances

    except Exception as e:
        log.error(e)
        raise e