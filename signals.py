import boto
from django.conf import settings
import os
from urlparse import urlparse
from .fields import S3FileField


# pre_delete.connect(s3_clean_model, sender=Resume)
def s3_clean_model(sender, instance, **kwargs):
    """
        This deletes the file from S3
    """
    # Get the connection information from settings
    s3 = boto.connect_s3(settings.AWS_ACCESS_KEY_ID,
                         settings.AWS_SECRET_ACCESS_KEY)
    # Get the bucket information from settings
    bucket = s3.lookup(settings.AWS_STORAGE_BUCKET_NAME)

    # Get any fields that are an S3FileField from the model instance.
    fields = [f for f in instance.__class__._meta.fields if isinstance(
        f, S3FileField)]

    # Loop through the fields, and delete all the files associated with the
    # fields.
    for _field in fields:
        field = getattr(instance, _field.name)  # Get the field

        f = urlparse(
            field.url).path  # Get the file path by splitting it from the S3 url.
        fname = os.path.basename(f)  # Get the file name

        # Actually tell the bucket to delete the keys
        key1 = bucket.delete_key(f)
        key2 = bucket.delete_key(f.split(fname)[0])
        # Make sure the delete returned an object.
        assert(bool(key1))
        assert(bool(key2))
