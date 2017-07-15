#!/usr/bin/env python

### Code taken from http://wescpy.blogspot.com/2015/12/migrating-to-new-google-drive-api-v3.html and modified

from __future__ import print_function
import os

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

def main(file_loc, folder_id):
    try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None

    SCOPES = 'https://www.googleapis.com/auth/drive.file'
    store = file.Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store, flags) \
                if flags else tools.run(flow, store)
    DRIVE = build('drive', 'v3', http=creds.authorize(Http()))

    # FILES = (
    #     ('./map/FULL_MAP_DATA.txt', 'application/vnd.google-apps.document'),
    #     ('./map/FULL_MAP.png', None),
    # )
    FILES = (
          (file_loc, None),
    )

    for filename, mimeType in FILES:
        if len(folder_id) > 1:
            metadata = {
                'name': filename,
                'parents': [ folder_id ]
            }
        else: 
            metadata = {
                'name': filename,
            }
        if mimeType:
            metadata['mimeType'] = mimeType
        res = DRIVE.files().create(body=metadata, media_body=filename).execute()
        if res:
            print('Uploaded "%s" (%s)' % (filename, res['mimeType']))

def create_folder(folder_tag):
    try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None

    SCOPES = 'https://www.googleapis.com/auth/drive.file'
    store = file.Storage('storage.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store, flags) \
                if flags else tools.run(flow, store)
    DRIVE = build('drive', 'v3', http=creds.authorize(Http()))
    
    file_metadata = {
        'name' : 'map_data_' + folder_tag,
        'mimeType' : 'application/vnd.google-apps.folder'
    }
    res = DRIVE.files().create(body=file_metadata,fields='id').execute()
    print ('Folder ID: ' + res.get('id'))
    return res.get('id')


# if __name__ == '__main__':
    # create_folder('')