from django.test import TestCase
from django.core.files import File
from django.conf import settings
import hashlib
import os
from django.db import models
from s3filefield.fields import S3FileField
from s3filefield.signals import s3_clean_model_function


class S3TestModel(models.Model):
    extra = models.CharField(max_length=10)
    s3file = S3FileField()
    s3file2 = S3FileField(s3_fields=['extra'])


class S3FieldTest(TestCase):

    def setup_databases(self, **kwargs):
        """ Override the database creation defined in parent class """
        pass

    def teardown_databases(self, old_config, **kwargs):
        """ Override the database teardown defined in parent class """
        pass

    def setUp(self):
        self.filedir, self.filename = os.path.split(os.path.realpath(__file__))

        # precalculate the file hash
        self._f = open('%s/__init__.py' % self.filedir, 'r')
        sha1 = hashlib.sha1()
        for chunk in iter(lambda: self._f.read(8192), b''):
            sha1.update(chunk.encode('base64'))
        self.sha1 = sha1.hexdigest()
        self._f.close()

        self.bucket = settings.AWS_STORAGE_BUCKET_NAME
        self.correct_s3file = "py/%s/__init__.py" % self.sha1
        self.correct_s3file2 = "loremipsum/py/%s/__init__.py" % self.sha1

        self.file = File(open('%s/__init__.py' % self.filedir, 'r'))

    def test_backend(self):
        testmodel = S3TestModel()
        testmodel.extra = 'loremipsum'

        testmodel.s3file = self.file
        testmodel.s3file2 = self.file
        testmodel.s3file.save("__init__.py", self.file)
        testmodel.s3file2.save("__init__.py", self.file)

        testmodel.save()
        self.assertIn(self.correct_s3file, testmodel.s3file.url)
        self.assertIn(self.correct_s3file2, testmodel.s3file2.url)

        self.assertIn(self.bucket, testmodel.s3file.url)
        self.assertIn(self.bucket, testmodel.s3file2.url)
        s3_clean_model_function(testmodel)

    def tearDown(self):
        self.file.close()
