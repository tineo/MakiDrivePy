__author__ = 'tineo'

import httplib2
import json
from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials
from makidifile import Makidifle
from makidlist import Makidlist

with open('config.json') as data_file:
    data = json.load(data_file)


with open(data.get("authentication").get("p12_src")) as f:
    private_key = f.read()

credentials = SignedJwtAssertionCredentials(data.get("authentication").get("client_mail"),
                                            private_key,
                                            'https://www.googleapis.com/auth/drive')

http = httplib2.Http()
http = credentials.authorize(http)

drive_service = build('drive', 'v2', http=http)

file_list = data.get("files")

for dn in file_list:

    mk = Makidifle()
    mklist = Makidlist(drive_service)
    mklist.list(dn.get("path"), dn.get("folder_id"))


