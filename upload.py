#!/usr/bin/env python

import os
import boto3
import sys
session = boto3.session.Session()


#############
# Functions #
#############

# If the upload cannot even be run just fail the job
def core_fail(message):
    print(message)
    sys.exit(1)

#############
# Variables #
#############

global region
global bucket
region = 'ams3'
bucket = 'lsio-ci'

# Make sure all needed env variables are set
def check_env():
    try:
        global spaces_key
        global spaces_secret
        global file_name
        global destination
        global mimetype
        mimetype = os.environ["MIMETYPE"]
        destination = os.environ["DESTINATION"]
        file_name = os.environ["FILE_NAME"]
        spaces_key = os.environ["ACCESS_KEY"]
        spaces_secret = os.environ["SECRET_KEY"]
    except KeyError as error:
        core_fail(str(error) + ' is not set in ENV')

# Upload blob to DO Spaces
def blob_upload():
    print('Uploading File')
    spaces = session.client(
        's3',
        region_name=region,
        endpoint_url='https://' + region + '.digitaloceanspaces.com',
        aws_access_key_id=spaces_key,
        aws_secret_access_key=spaces_secret)
    # File upload
    try:
        spaces.upload_file(
            '/mnt/' + file_name,
            bucket,
            destination,
            ExtraArgs={'ContentType': mimetype, 'ACL': "public-read"})
    except Exception as error:
        core_fail('Upload Error ' + str(error))

##############
# Main Logic #
##############
check_env()
blob_upload()
