import os

from django.core.files.storage import FileSystemStorage
from django.conf import settings


class OverWriteStorage(FileSystemStorage):
    def _save(self, name, content):
        if len(self.path(name)) > 60000:
            raise PermissionError('too much files in directory')
        else:
            return super(OverWriteStorage, self)._save(name, content)

    def get_valid_name(self, name):
        return 'picture.' + name.split('.')[1]
