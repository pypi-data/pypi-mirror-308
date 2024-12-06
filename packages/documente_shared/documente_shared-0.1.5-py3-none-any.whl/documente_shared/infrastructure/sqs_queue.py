import json
from dataclasses import dataclass

import boto3


@dataclass
class SQSQueue(object):
    queue_url: str

    def __post_init__(self):
        self._client = boto3.client('sqs')

    def send_message(
        self,
        payload: dict,
        message_attributes: dict = None,
        delay_seconds: dict = None,
        message_group_id: dict = None,
        message_deduplication_id: dict =None,
    ):
        message_params = {
            'QueueUrl': self.queue_url,
            'MessageBody': json.dumps(payload),
            'MessageAttributes': message_attributes,
            'DelaySeconds': delay_seconds,
            'MessageGroupId': message_group_id,
            'MessageDeduplicationId': message_deduplication_id,
        }
        clean_params = {key: value for key, value in message_params.items() if value}  # noqa: E501, WPS110
        return self._client.send_message(**clean_params)