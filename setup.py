try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='S3FileField',
    version='1.0.0',
    author='Tyrel Souza',
    author_email='tsouza@propelmarketing.com',
    packages=['s3filefield',],
    url='http://www.propelmarketing.com',
    license='LICENSE.txt',
    description='Specify which fields are an S3 field rather than default to all.',
    long_description=open('README.txt').read(),
    install_requires = [
       'Django==1.5.1',
       'boto==2.9.7',
       'django-storages==1.1.8'
    ]
)
