import logging

from pathlib import Path

from kino.utils.check_s3 import connection_to_s3
from kino.utils.check_urls_to_quality import urls_to_quality
from kino.enums import QualityChoose
from kino.video.s3.s3_client import s3_current_client


def upload_video(output_file, media):

    quality_map = {
        "360": QualityChoose.very_low,
        "480": QualityChoose.low,
        "720": QualityChoose.average,
        "1080": QualityChoose.high,
    }

    if connection_to_s3():
        quality = Path(output_file).name.split(".")[-2]
        if quality in quality_map:
            quality_choose = quality_map[quality]
            s3_current_client.upload_video(output_file, quality_choose, media)
            info_unload = f"{media.card.name} - {quality_choose} was unload"
            logging.info(info_unload)
        else:
            logging.error("Quality wasn't find")

    else:
        quality = Path(output_file).name.split("_")[-1].split(".")[0]
        if quality in quality_map:
            quality_choose = quality_map[quality]
            urls_to_quality(media, quality_choose, output_file)
            info_added = f"{media.card.name} - {quality_choose} was added"
            logging.info(info_added)
        else:
            logging.error("Quality wasn't find")
