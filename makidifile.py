__author__ = 'tineo'

from os import popen
import sys
from apiclient.http import MediaFileUpload
from os.path import join
from mimetypes import MimeTypes

class Makidifle:

    def __init__(self):
        self.mime = MimeTypes()

    def insert(self, file_name, path_name, folder_id, drive_service):
        file_path = join(path_name, file_name)
        mime_type = self.mime.guess_type(file_path)

        if mime_type[0] is not None:
            media_body = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)

            sys.stdout.write("Folder: %s\n" % file_path)
            sys.stdout.write("File: %s\n" % file_name)
            sys.stdout.flush()

            body = {'title': file_name,
                    'parents': [{'id': folder_id}]
            }

            request = drive_service.files().insert(body=body, media_body=media_body)

            rows, columns = popen('stty size', 'r').read().split()
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    rows, columns = popen('stty size', 'r').read().split()
                    len_bar = int(int(columns) / 3)
                    bar = '=' * int(status.progress() * len_bar) + '-' * (len_bar - int(status.progress() * len_bar))
                    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, int(status.progress() * 100), '%', file_name))
                    sys.stdout.flush()

            sys.stdout.write('[%s] %s%s ...%s\n' % ('=' * int(int(columns)/3), 100, '%', file_name))

    def create_folder(self, folder_name, folder_id, drive_service) :
        body = {
            'title': folder_name,
            'mimeType': "application/vnd.google-apps.folder",
            "parents": [{'id': folder_id}]
        }

        request = drive_service.files().insert(body=body).execute()
        return request['id']


