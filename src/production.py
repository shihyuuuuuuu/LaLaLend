from .settings import *


ALLOWED_HOSTS = ['*']

DOMAIN = "https://lala-lend.herokuapp.com"

# Heroku: Update database configuration from $DATABASE_URL.
import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# AWS bucket settings
AWS_QUERYSTRING_AUTH = False
AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
AWS_STORAGE_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/'
MEDIA_ROOT = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/'
MEDIA_DOMAIN = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/'
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"