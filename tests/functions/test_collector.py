import ec2collector.functions.collector

from unittest import TestCase
from unittest.mock import MagicMock, patch
from ec2collector.functions.collector import (
    put_tag_info,
    collect
)


class TestCollect(TestCase):

    def test_put_tag_info(self):
        instances = [
            {"InstanceId": 'i-xxx', "Tags": [{"Key": 'tagA', "Value": "001-a"}, {"Key": 'tagB', "Value": "001"}]},
            {"InstanceId": 'i-yyy', "Tags": [{"Key": 'require_action', "Value": "true"}, {"Key": 'tagB', "Value": "002"}]},
            {"InstanceId": 'i-zzz', "Tags": [{"Key": 'require_action', "Value": "false"}, {"Key": 'tagB', "Value": "003"}]},
        ]
        m_table = MagicMock()
        with patch('boto3.resource') as m_rsc:
            # TODO なんとかする
            put_tag_info(m_table, instances)
            # print(m_rsc.return_value.Table.return_value.batch_writer.return_value.__enter__.return_value.put_item.called)
            # print(m_rsc.return_value.Table.return_value.batch_writer.called)