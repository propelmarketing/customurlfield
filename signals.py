import boto
from django.conf import settings
import os
from urlparse import urlparse
from .fields import S3FileField

#pre_delete.connect(s3_clean_model, sender=Resume)
def s3_clean_model(sender, instance, **kwargs):
    s3 = boto.connect_s3(settings.AWS_ACCESS_KEY_ID,
                         settings.AWS_SECRET_ACCESS_KEY)
    bucket = s3.lookup(settings.AWS_STORAGE_BUCKET_NAME)
    fields = [f for f in instance.__class__._meta.fields if isinstance(f, S3FileField)]
    for _field in fields:
        field = getattr(instance, _field.name)
        f = urlparse(field.url).path
        fname = os.path.basename(f)
        key1 = bucket.delete_key(f)
        key2 = bucket.delete_key(f.split(fname)[0])
        assert(bool(key1))
        assert(bool(key2))
