import logging
import boto3

from botocore.client import Config
from django.conf import settings


# скачивание файла с minIO с помощью boto3
def download_video_from_s3(media, destination_path):
    try:
        file_name = media.source_link.split("/")[-1]
        s3 = boto3.client("s3",
                          endpoint_url=settings.AWS_S3_CUSTOM_DOMAIN,
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          config=Config(signature_version="s3v4"),
                          region_name=settings.AWS_S3_REGION_NAME
                          )
        s3.download_file(f"{settings.AWS_STORAGE_BUCKET_NAME}",
                         f"source/{file_name}",
                         f"{destination_path}/{file_name}")
        return f"{destination_path}/{file_name}"
    except Exception:
        logging.exception("Error during download video from S3")
