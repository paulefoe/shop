import os
import errno

from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.core.files.move import file_move_safe
from django.utils.encoding import force_text
from django.utils.crypto import get_random_string
from django.utils._os import safe_join


class OverWriteStorage(FileSystemStorage):
    def save(self, name, content, max_length=None):
        if name is None:
            name = content.name
        print(name, '          this is name')
        if not hasattr(content, 'chunks'):
            content = File(content, name)
        print(content, '     this is content')

        name = self.get_available_name(name, max_length=max_length)
        print(name, '  this is not a final name')

        full_path = self.path(name)
        directory = os.path.dirname(full_path)
        print(directory, 'this is directory')
        if len(os.listdir(directory)) > 2:
            temp = name.split('/')
            new_folder = temp[0] + get_random_string(3)
            name = os.path.join(new_folder, temp[1])
        print(name, '  this is final name')
        return self._save(name, content)

    def get_valid_name(self, name):
        return 'picture.' + name.split('.')[-1]


