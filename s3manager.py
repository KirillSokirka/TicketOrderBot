import boto3
import os


session = boto3.Session(
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'))


s3 = session.resource('s3')


def upload_object(file_name):
    object = s3.Object(os.getenv('AWS_STORAGE_BUCKET_NAME'), 'events.json')\
        .upload_file(Filename='json_files/events.json')
