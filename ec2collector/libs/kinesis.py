import json
from uuid import uuid4
import boto3
from boto3_type_annotations.kinesis import Client as KinesisClient
from botocore.exceptions import ClientError
from ec2collector import settings

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

kinesis: KinesisClient = None

def _get_kinesis_client():
    global kinesis
    if kinesis is None:
        kinesis = boto3.client('kinesis')
    return kinesis


def put_action_record(instance):
    """
    Kinesis にアクション対象のインスタンス情報を送りつけたい関数
    実際のアクションは Consumer 側で関知せず、ストリームの受け側で非同期に何かしらやる

    :param instance: {'InstanceId': <str>, 'Tags': [<Tag-dict>]}
    :type instance: dict
    """
    # kinesis_client: kinesisClient = _get_kinesis_client()
    # kinesis_client.put_record(
    #     StreamName=settings.ACTION_STREAM,
    #     PartitionKey=str(uuid4()),
    #     Data=instance
    # )
    log.info(f"something awesome: ${json.dumps(instance)}")
