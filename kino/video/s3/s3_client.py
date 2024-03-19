from django.conf import settings

from kino.video.s3.storages import S3Client

s3_current_client = S3Client(settings.AWS_STORAGE_BUCKET_NAME)
