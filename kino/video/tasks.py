import logging
from pathlib import Path
from config import celery_app
from config.settings import base

from kino.video.models import Media, Task
from kino.enums import StatusChoose
from kino.utils.download_video import download_video_from_s3
from kino.utils.record_video import record_video
from kino.utils.upload_video import upload_video
from kino.utils.check_s3 import connection_to_s3

media_path = base.PATH_TO_MEDIA


@celery_app.task()
def download_video(media_id):
    media = Media.objects.get(id=media_id)
    logging.info(f"Start download {media.card.name}")
    destination_path = Path(media_path) / "source" / media.card.name
    try:
        if not Path(destination_path).exists():
            if connection_to_s3():
                Task.objects.create(media=media, status=StatusChoose.processing)
                logging.info("Download started from S3")
                video_path = download_video_from_s3(media, destination_path)
            else:
                video_path = media.source_link
                logging.info("Downloading from local machine")
                Task.objects.create(media=media, status=StatusChoose.processing)
                encode_video.delay(video_path, media_id)
        else:
            logging.error(f"File was downloading yet. Please check directory — {destination_path}")
    except Exception:
        Task.objects.filter(media=media).update(status=StatusChoose.failed)
        logging.exception(f"Error with download {media.card.name}")


@celery_app.task()
def encode_video(video_path, media_id):
    logging.info(f"Media in task of encode - {media_id}")
    record_video(video_path, media_id)


@celery_app.task()
def save_or_upload_quality(output_files, media_id):
    media = Media.objects.get(id=media_id)
    upload_video(output_files, media)
