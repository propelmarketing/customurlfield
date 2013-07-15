from django.test import TestCase
from django.db import models
from .fields import S3FileField

class S3Model(models.Model):
    extra = models.CharField()
    s3file = S3FileField()
    s3file2 = S3FileField(s3_fields=['extra'])

class S3FieldTest(TestCase):
    def test_backend(self):
        mode = S3Model()
        mode.save()
