import logging
from pathlib import Path
from config import celery_app
from django.conf import settings

from kino.video.models import Media, Task
from kino.enums import StatusChoose
from kino.utils import record_video, connection_to_s3, download_video_from_s3

media_path = settings.PATH_TO_MEDIA


@celery_app.task()
def download_video(media_id):
    media = Media.objects.get(id=media_id)
    info_start_work = f"Start work with {media.card.name}"
    logging.info(info_start_work)
    # потом сделать с англ названием наверное подумать, так как с русским папка не создаётся
    destination_path = Path(media_path) / "source" / media.card.name
    try:
        if not Path(destination_path).exists():
            if connection_to_s3():
                Task.objects.create(media=media, status=StatusChoose.processing)
                logging.info("Download started from S3")
                video_path = download_video_from_s3(media, destination_path)
            else:
                video_path = media.source_link
                logging.info("Start work with video from local machine")
                Task.objects.create(media=media, status=StatusChoose.processing)
                encode_video.delay(video_path, media_id)
        else:
            logging.error("File was downloading yet. Please check directory again")
    except Exception:
        Task.objects.filter(media=media).update(status=StatusChoose.failed)
        logging.exception("Error during download")


@celery_app.task()
def encode_video(video_path, media_id):
    record_video(video_path, media_id)
