import logging
from pathlib import Path

from django.conf import settings

from kino.enums import QualityChoose
from kino.utils.s3.check_s3 import connection_to_s3
from kino.utils.s3.storages import s3_current_client
from kino.utils.stages_of_video.check_urls_to_quality import urls_to_quality


def upload_video(output_file, media):
    output_file = Path(output_file)
    quality_map = {
        "360": QualityChoose.very_low,
        "480": QualityChoose.low,
        "720": QualityChoose.average,
        "1080": QualityChoose.high,
    }
    if connection_to_s3():
        quality = output_file.name.split(".")[-2]
        if quality in quality_map:
            quality_choose = quality_map[quality]
            path_s3 = s3_current_client.upload_video(output_file, media)
            urls_to_quality(
                media,
                quality_choose,
                f"{settings.AWS_S3_ENDPOINT_URL}/{settings.AWS_STORAGE_BUCKET_NAME}/{path_s3}",
            )
            info_unload = f"{media.card.name} - {quality_choose} was unload"
            logging.info(info_unload)
        else:
            logging.error("Quality wasn't find")
    else:
        quality = output_file.name.split(".")[-2]
        if quality in quality_map:
            quality_choose = quality_map[quality]
            urls_to_quality(media, quality_choose, output_file)
            info_added = f"{media.card.name} - {quality_choose} was added"
            logging.info(info_added)
        else:
            logging.error("Quality wasn't find")
