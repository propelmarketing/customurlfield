#-*- coding: utf-8 -*-
from django.db import models
import hashlib


class S3FileField(models.FileField):
    description = "S3 File Field"

    def __init__(self, s3_fields=[], *args, **kwargs):
        """
        Setup the S3FileField with parameters and a max_length
        if s3_fields provided, loops through and gets those attrs.
        """
        self.s3_fields = s3_fields
        kwargs['upload_to'] = self.upload_to
        super(S3FileField, self).__init__(*args, **kwargs)

    def upload_to(self, instance, filename):
        path_fields = []
        field = getattr(instance, self.name)
        for attr in self.s3_fields:
            try:
                path_fields.append(getattr(instance, attr))
            except:
                raise ValueError("Incorrect model attribute '%s' in s3_fields" % attr)

        sha1 = hashlib.sha1()
        for chunk in iter(lambda: field.file.read(8192), b''):   # NEED TO FIX THIS ATTR
            sha1.update(chunk.encode('base64'))
        file_hash = sha1.hexdigest()

        path_fields.extend([filename.split(".")[-1],
                            file_hash,
                            filename])
        return "/".join(path_fields)
