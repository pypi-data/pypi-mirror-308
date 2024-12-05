from dataclasses import dataclass
from typing import Optional

from python_layer.python import boto3

def remove_none_values(data: dict) -> dict:  # noqa: WPS110
    return {key: value for key, value in data.items() if value is not None}  # noqa: WPS110


@dataclass
class S3Bucket(object):
    bucket_url: str

    def __post_init__(self):
        self._resource = boto3.resource('s3')


    def get(self, file_name: str):
        return self._resource.Object(self.bucket_url, file_name).get()

    def upload(self, file_name, file_content, content_type: Optional[str] = None):
        optional_params = {'ContentType': content_type}
        return self._resource.Object(self.bucket_url, file_name).put(
            Body=file_content,
            **remove_none_values(optional_params),
        )

    def delete(self, file_name):
        return self._resource.Object(self.bucket_url, file_name).delete()

    def get_url(self, file_name):
        return 'https://{bucket_url}.s3.amazonaws.com/{file_name}'.format(
            bucket_url=self.bucket_url,
            file_name=file_name,
        )

    def read(self, file_name):
        return self.get(file_name)['Body'].read()
