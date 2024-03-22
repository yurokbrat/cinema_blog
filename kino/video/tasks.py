import logging
from pathlib import Path

from django.conf import settings

from config import celery_app
from kino.enums import StatusChoose
from kino.utils.other.create_folder import get_media_folders
from kino.utils.s3.check_s3 import connection_to_s3
from kino.utils.s3.s3_client import s3_current_client
from kino.utils.stages_of_video.record import record_video
from kino.video.models import Media, Task

media_path = settings.PATH_TO_MEDIA


@celery_app.task()
def download_video(media_id):
    media = Media.objects.get(id=media_id)
    info_start_work = f"Start work with {media.card.name}"
    logging.info(info_start_work)
    task = Task.objects.create(
        media=media,
        status=StatusChoose.processing,
    )
    try:
        if connection_to_s3():
            logging.info("Download started from MinIO")
            directory_name, content_type_folder = get_media_folders(media)
            destination_path = Path(
                media_path,
                "source",
                content_type_folder,
                directory_name,
            )
            destination_path.mkdir(parents=True, exist_ok=True)
            video_path = s3_current_client.download_video(
                media,
                destination_path,
            )
            encode_video.delay(video_path, media_id, task.id)
        else:
            video_path = media.source_link
            logging.info("Start work with video from local machine")
            encode_video.delay(video_path, media_id)
    except Exception:
        task.status = StatusChoose.failed
        task.save()
        logging.exception("Error during download")


@celery_app.task()
def encode_video(video_path, media_id, task_id):
    record_video(video_path, media_id, task_id)
