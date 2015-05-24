__author__ = 'tineo'
from os import listdir
from os.path import isfile, isdir, join
from makidifile import Makidifle
from os.path import basename, dirname

class Makidlist :

    def __init__(self, drive_service):
        self.mk = Makidifle()
        self.ds = drive_service

    def list_files(self, file_path):
        return [f for f in listdir(file_path) if isfile(join(file_path, f))]

    def list_dirs(self, file_path):
        return [f for f in listdir(file_path) if isdir(join(file_path, f))]

    def list(self, file_path, folder_id):
        if isdir(file_path):
            for f in listdir(file_path):
                if isdir(join(file_path, f)):
                    self.list(join(file_path, f), self.mk.create_folder(f, folder_id, self.ds))
                elif isfile(join(file_path, f)):
                    self.mk.insert(f, file_path, folder_id, self.ds)
        else:
            self.mk.insert(basename(file_path), dirname(file_path), folder_id, self.ds)

