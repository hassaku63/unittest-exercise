from unittest import TestCase
from unittest.mock import MagicMock, call
from ec2collector.functions.collector import put_tag_info


class TestCollect(TestCase):

    def test_put_tag_info(self):
        instances = [
            {"InstanceId": 'i-xxx', "Tags": [{"Key": 'tagA', "Value": "001-a"}, {"Key": 'tagB', "Value": "001"}]},
            {"InstanceId": 'i-yyy', "Tags": [{"Key": 'require_action', "Value": "true"}, {"Key": 'tagB', "Value": "002"}]},
            {"InstanceId": 'i-zzz', "Tags": [{"Key": 'require_action', "Value": "false"}, {"Key": 'tagB', "Value": "003"}]},
        ]
        m_table = MagicMock()

        put_tag_info(m_table, instances)
        called_args = m_table.batch_writer.return_value.__enter__.return_value.put_item.call_args_list
        assert called_args[0] == call(Item={'InstanceId': 'i-xxx', 'Tags': [{'Key': 'tagA', 'Value': '001-a'}, {'Key': 'tagB', 'Value': '001'}]})
        assert called_args[1] == call(Item={"InstanceId": 'i-yyy', "Tags": [{"Key": 'require_action', "Value": "true"}, {"Key": 'tagB', "Value": "002"}]})
        assert called_args[2] == call(Item={"InstanceId": 'i-zzz', "Tags": [{"Key": 'require_action', "Value": "false"}, {"Key": 'tagB', "Value": "003"}]})
