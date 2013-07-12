# This is a Django FileField model field with custom S3 Attributes.

More coming later.


## To Use

### Example
    class Resume(models.Model):
        name = models.CharField(max_length=256)
        product = models.CharField(max_length=256)
        pdf = S3FileField(s3_fields=['name', 'product'])
