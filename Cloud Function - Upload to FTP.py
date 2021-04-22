import pickle
import pandas as pd
# Imports Python standard library logging
import logging
from google.cloud import storage
from datetime import datetime, timedelta
import datetime as dt
from dateutil.relativedelta import relativedelta
from google_auth_oauthlib.flow import InstalledAppFlow
from apiclient.discovery import build
import pysftp
from io import StringIO
import paramiko

def upload_file(event, context):
    
    file = event
    file_name = file['name']
    
    client = storage.Client()
    bucket = client.get_bucket('BUCKET NAME')

    bucket2 = client.get_bucket('BUCKET NAME')
    blob2 = bucket2.blob('KEY FILE NAME')
    contents = blob2.download_as_string()
    contents = contents.decode(encoding='UTF-8')

    fileblob2 = bucket.blob(file_name)

    key_file = StringIO(contents)

    private_key_file = paramiko.RSAKey.from_private_key(key_file)
    
    hostname = 'HOSTNAME'
    username = 'USERNAME'
    
    def sftptransfer():
        cnopts = pysftp.CnOpts()
        cnopts.hostkeys = None  
        with pysftp.Connection(hostname, username=username, private_key=private_key_file, cnopts=cnopts) as sftp:

            remote_file=sftp.open(file_name, 'w+')
            fileblob2.download_to_file(remote_file)

            sftp.close()
    sftptransfer()  
   
    return f'Sucess!'

