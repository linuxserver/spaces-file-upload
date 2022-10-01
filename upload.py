#!/usr/bin/env python3

import os
import boto3
from boto3.exceptions import S3UploadFailedError
from botocore.exceptions import ClientError

def file_upload():
    """Upload file to S3 bucket"""
    print('Uploading File')        
    try:
        s3_client.upload_file(
            f'/mnt/{file_name}',
            bucket,
            destination,
            ExtraArgs={'ContentType': mimetype, 'ACL': "public-read"})
        print(f'Uploading "{file_name}" finished')
    except (S3UploadFailedError, ClientError, Exception) as error:
        print(f'Upload Error {error}')
        raise error from error
    
if __name__ == '__main__':
    try:
        mimetype = os.environ["MIMETYPE"]
        destination = os.environ["DESTINATION"]
        file_name = os.environ["FILE_NAME"]
        S3_key = os.environ["ACCESS_KEY"]
        S3_secret = os.environ["SECRET_KEY"]  
    except KeyError as error:
        print(f'{error} is not set in ENV')
        raise error
    region = os.environ.get('S3_REGION', 'us-east-1')
    bucket = os.environ.get('S3_BUCKET', 'ci-tests.linuxserver.io')
    s3_client = boto3.Session().client('s3',region_name=region,aws_access_key_id=S3_key,aws_secret_access_key=S3_secret)
    file_upload()