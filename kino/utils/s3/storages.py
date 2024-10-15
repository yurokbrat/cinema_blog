from pathlib import Path

import boto3
from botocore.config import Config
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage

from kino.utils.other.create_folder import get_media_folders
from kino.utils.other.generate_hide_url import (
    media_url_generate,
    upload_to_s3,
)


class CustomS3Boto3Storage(S3Boto3Storage):
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)
        if settings.MINIO_ACCESS_URL:
            self.secure_urls = False
            self.custom_domain = settings.MINIO_ACCESS_URL


class S3Client:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.client = boto3.client(
            "s3",
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            config=Config(signature_version="s3v4"),
            region_name=settings.AWS_S3_REGION_NAME,
        )

    def download_video(self, media, destination_path):
        file_name = media.source_link.split("/")[-1]
        source_file = f"source/{file_name}"
        path_to_file = Path(destination_path, file_name)
        self.client.download_file(self.bucket_name, source_file, path_to_file)
        return f"{destination_path}/{file_name}"

    def upload_video(self, output_file, media):
        # Создаём допустимое название для bucket в S3
        directory_name, content_type_folder = get_media_folders(media)
        bucket_name = media_url_generate()
        file = upload_to_s3(bucket_name, output_file.name)
        path_s3 = f"{content_type_folder}/{file}"
        self.client.upload_file(output_file, self.bucket_name, path_s3)
        return path_s3


s3_current_client = S3Client(settings.AWS_STORAGE_BUCKET_NAME)
