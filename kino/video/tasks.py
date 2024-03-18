import logging
import re
from pathlib import Path
from config import celery_app
from django.conf import settings

from kino.cards.models import Film
from kino.video.models import Media, Task
from kino.enums import StatusChoose
from kino.utils import record_video, connection_to_s3, download_video_from_s3

media_path = settings.PATH_TO_MEDIA


@celery_app.task()
def download_video(media_id):
    media = Media.objects.get(id=media_id)
    info_start_work = f"Start work with {media.card.name}"
    logging.info(info_start_work)
    task = Task.objects.create(media=media, status=StatusChoose.processing)
    try:
        if connection_to_s3():
            logging.info("Download started from MinIO")
            directory_name = re.sub(r'[:"/\\|?*]', '', media.card.name) # noqa: Q000
            content_type_model = media.content_type.model_class()
            content_type_folder = "films" if content_type_model == Film else "serials"
            destination_path = Path(media_path) / "source" / content_type_folder / directory_name
            if not Path(destination_path).exists():
                destination_path.mkdir(parents=True, exist_ok=True)
                video_path = download_video_from_s3(media, destination_path)
                encode_video.delay(video_path, media_id, task.id)
            else:
                logging.error("File was downloading yet. Please check directory again")
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
