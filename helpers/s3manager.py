import boto3
import os


session = boto3.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))
s3 = session.resource('s3')


class S3Manager:

    @staticmethod
    def download_object(file_name, key):
        s3.Bucket(os.getenv('AWS_STORAGE_BUCKET_NAME')).download_file(key, file_name)

    @staticmethod
    def upload_object(file_name, key):
        s3.Object(os.getenv('AWS_STORAGE_BUCKET_NAME'), key).upload_file(Filename=file_name)
