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
        # Set the fields for the attrs to grab
        self.s3_fields = s3_fields

        # if there was not an upload_to supplied, use our built in function
        if not kwargs.get('upload_to', None):
            kwargs['upload_to'] = self._upload_to

        super(S3FileField, self).__init__(*args, **kwargs)

    def upload_to(self, instance, filename):
        """
            Sets the upload
        """

        path_fields = []

        # Get the field from the instance
        field = getattr(instance, self.name)

        # Loop through the fields on the model to get values for the url
        # partitioning.
        for attr in self.s3_fields:
            try:
                path_fields.append(getattr(instance, attr))
            except:
                # If it doesn't exist in the model, inform the user that the
                # attribute was wrong
                raise ValueError(
                    "Incorrect model attribute '%s' in s3_fields" % attr)

        # Hash the file so we don't get collisions (unlikely with the
        # partitioning we have, but still should account for it.)
        sha1 = hashlib.sha1()
        for chunk in iter(lambda: field.file.read(8192), b''):
            sha1.update(chunk.encode('base64'))
        file_hash = sha1.hexdigest()

        # Join the file path so we have the name to save it to in the S3
        # backend
        path_fields.extend([filename.split(".")[-1],
                            file_hash,
                            filename])
        return "/".join(path_fields)
