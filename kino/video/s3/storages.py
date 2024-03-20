import re
from pathlib import Path

import boto3
from botocore.config import Config
from django.conf import settings
from transliterate import translit

from kino.cards.models import Film
from kino.utils.check_urls_to_quality import urls_to_quality
from kino.utils.generate_hide_url import media_url_generate


class S3Client:
    def __init__(self, bucket_name):
        self.bucket_name = bucket_name
        self.client = boto3.client("s3",
                                   endpoint_url=settings.AWS_S3_ENDPOINT_URL,
                                   aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                   aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                   config=Config(signature_version="s3v4"),
                                   region_name=settings.AWS_S3_REGION_NAME)

    def get_media_folders(self, media):
        directory_name = re.sub(r'[:"/\\|?*]', '', media.card.name)
        content_type_model = media.content_type.model_class()
        content_type_folder = "films" if content_type_model == Film else "serials"
        if media.season:
            directory_name = f"{directory_name}/season_{media.season}"
            if media.episode:
                directory_name = f"{directory_name}/episode_{media.episode}"
        return directory_name, content_type_folder

    def download_video(self, media, destination_path):
        file_name = media.source_link.split("/")[-1]
        source_file = f"source/{file_name}"
        path_to_file = Path(destination_path, file_name)
        self.client.download_file(self.bucket_name, source_file, path_to_file)
        return f"{destination_path}/{file_name}"

    def upload_video(self, output_file, quality, media):
        # Создаём допустимое название для bucket в S3
        directory_name, content_type_folder = self.get_media_folders(media)
        transliterated_name = translit(media.card.name, "ru", reversed=True)
        bucket_name = re.sub(r'[^\w.-]', '_', transliterated_name).lower()
        file_name = Path(output_file).name
        # Проверяем, есть ли сезон и серия для создания дополнительных папок в S3
        if media.season:
            path_s3 = (f"{content_type_folder}/{bucket_name}/"
                       f"season_{media.season}/{file_name}")
            if media.episode:
                path_s3 = (f"{content_type_folder}/{bucket_name}/"
                           f"season_{media.season}/episode_{media.episode}/{file_name}")
        else:
            path_s3 = f"{content_type_folder}/{bucket_name}/{file_name}"
        self.client.upload_file(output_file, self.bucket_name, path_s3)
        encrypted_path_s3 = media_url_generate()
        urls_to_quality(media, quality,
                        f"{settings.AWS_S3_ENDPOINT_URL}/"
                        f"{settings.AWS_STORAGE_BUCKET_NAME}/"
                        f"{path_s3}",
                        f"{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/"
                        f"{content_type_folder}/{encrypted_path_s3}/{file_name}")
