#-*- coding: utf-8 -*-
from django.db import models
import hashlib


class S3FileField(models.FileField):
    description = "S3 File Field"

    def __init__(self, s3_fields=[], *args, **kwargs):
        """
        Setup the S3FileField with parameters and a max_length
        """
        self.s3_fields = s3_fields
        kwargs['upload_to'] = self.upload_to

        super(S3FileField, self).__init__(*args, **kwargs)

    def upload_to(self, instance, filename):
        path_fields = []
        for attr in self.s3_fields:
            path_fields.append(getattr(instance, attr))

        md5 = hashlib.md5()
        for chunk in iter(lambda: getattr(instance, self.name).file.read(8192), b''):   # NEED TO FIX THIS ATTR
            md5.update(chunk.encode('utf-8'))
        file_hash = md5.hexdigest()

        path_fields.extend([filename.split(".")[-1],
                            file_hash,
                            filename])
        return "/".join(path_fields)
