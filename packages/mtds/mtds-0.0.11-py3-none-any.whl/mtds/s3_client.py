import logging
import os

import boto3
from botocore.exceptions import NoCredentialsError


# TODO 单例模式
class S3Client:
    def __init__(self, cdn=None, **kwargs):
        self.cdn = cdn or 'https://d1n8x1oristvw.cloudfront.net'
        self.s3_client = boto3.client('s3', **kwargs)
        try:
            self.s3_client.list_buckets()
        except NoCredentialsError:
            raise Exception('No AWS credentials found')

    @classmethod
    def create_from_env(cls):
        aws_access_key_id = os.environ.get('aws_access_key_id')
        aws_secret_access_key = os.environ.get('aws_secret_access_key')

        if not aws_access_key_id or not aws_secret_access_key:
            raise Exception('AWS credentials not found in environment variables')

        return cls(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    def upload_file(self, file_path, s3_key, bucket_name='sing-strong', extra_args=None):
        self.s3_client.upload_file(
            file_path,
            bucket_name,
            s3_key,
            extra_args,
        )
        return f'{self.cdn}/{s3_key}'

    def upload_bytes(self, body, s3_key, bucket_name='sing-strong', **kwargs):
        self.s3_client.put_object(Bucket=bucket_name, Key=s3_key, Body=body, **kwargs)
        return f'{self.cdn}/{s3_key}'

    def download_file(self, s3_key, file_path, bucket_name='sing-strong', **kwargs):
        self.s3_client.download_file(bucket_name, s3_key, file_path, **kwargs)
