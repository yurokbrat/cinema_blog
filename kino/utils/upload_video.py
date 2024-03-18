import logging
import re
import boto3

from pathlib import Path
from botocore.config import Config
from django.conf import settings
from transliterate import translit

from kino.cards.models import Film
from kino.utils.check_s3 import connection_to_s3
from kino.video.models import VideoQuality
from kino.enums import QualityChoose


def upload_video(output_file, media):
    quality_map = {
        "360": QualityChoose.very_low,
        "480": QualityChoose.low,
        "720": QualityChoose.average,
        "1080": QualityChoose.high,
    }

    if connection_to_s3():
        s3 = boto3.client("s3",
                          endpoint_url=settings.AWS_S3_CUSTOM_DOMAIN,
                          aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                          config=Config(signature_version="s3v4"),
                          region_name=settings.AWS_S3_REGION_NAME
                          )
        # Создаём допустимое название для bucket в S3
        transliterated_name = translit(media.card.name, "ru", reversed=True)
        bucket_name = re.sub(r'[^\w.-]', '_', transliterated_name).lower() # noqa: Q000
        content_type_model = media.content_type.model_class()
        content_type_folder = "films" if content_type_model == Film else "serials"
        quality = Path(output_file).name.split(".")[-2]
        if quality in quality_map:
            quality_choose = quality_map[quality]
            s3.upload_file(output_file, settings.AWS_STORAGE_BUCKET_NAME,
                           f"{content_type_folder}/{bucket_name}/{Path(output_file).name}")
            VideoQuality.objects.create(media=media,
                                        quality=quality_choose,
                                        video_url=f"{settings.AWS_S3_CUSTOM_DOMAIN}/"
                                                  f"{settings.AWS_STORAGE_BUCKET_NAME}/"
                                                  f"{content_type_folder}/"
                                                  f"{bucket_name}/"
                                                  f"{Path(output_file).name}")
            info_unload = f"{media.card.name} - {quality_choose} was unload"
            logging.info(info_unload)
        else:
            logging.error("Quality wasn't find")

    else:
        quality = Path(output_file).name.split("_")[-1].split(".")[0]
        if quality in quality_map:
            quality_choose = quality_map[quality]
            VideoQuality.objects.create(media=media, quality=quality_choose, video_url=output_file)
            info_added = f"{media.card.name} - {quality_choose} was added"
            logging.info(info_added)
        else:
            logging.error("Quality wasn't find")
