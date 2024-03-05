import logging
import boto3
from pathlib import Path

from .check_s3 import connection_to_s3
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
        s3 = boto3.client("s3")
        bucket_name = "bucket_name"
        quality = Path(output_file).name.split("_")[-1].split(".")[0]
        if quality in quality_map:
            quality_choose = quality_map[quality]
            s3.upload_file(output_file, bucket_name, output_file.split("/")[-1])
            VideoQuality.objects.create(media=media, quality=quality_choose,
                                        video_url=f"https://s3.amazonaws.com/{bucket_name}/{output_file.split('/')[-2]}")
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
