# from django.test import TestCase
from django.test import TestCase
from django.core.files import File
from django.conf import settings

import os
from django.db import models
from s3filefield.fields import S3FileField


class S3TestModel(models.Model):
    extra = models.CharField(max_length=10)
    s3file = S3FileField()
    s3file2 = S3FileField(s3_fields=['extra'])


class S3FieldTest(TestCase):
    def setUp(self):
        self.bucket = settings.AWS_STORAGE_BUCKET_NAME
        self.filedir, self.filename = os.path.split(os.path.realpath(__file__))
        self.correct_s3file = "py/58cfd071c701994de308f82a83237258d26dc8d4/__init__.py"
        self.correct_s3file2 = "loremipsum/py/58cfd071c701994de308f82a83237258d26dc8d4/__init__.py"


    def setup_databases(self, **kwargs):
        """ Override the database creation defined in parent class """
        pass

    def teardown_databases(self, old_config, **kwargs):
        """ Override the database teardown defined in parent class """
        pass

    def test_backend(self):
        f = File(open('%s/__init__.py' % self.filedir, 'r'))
        testmodel = S3TestModel()
        testmodel.extra = 'loremipsum'

        testmodel.s3file = f
        testmodel.s3file2 = f

        testmodel.s3file.save("__init__.py", f)
        testmodel.s3file2.save("__init__.py", f)
        f.close()

        testmodel.save()
        self.assertIn(self.correct_s3file, testmodel.s3file.url)
        self.assertIn(self.correct_s3file2, testmodel.s3file2.url)

        self.assertIn(self.bucket, testmodel.s3file.url)
        self.assertIn(self.bucket, testmodel.s3file2.url)

