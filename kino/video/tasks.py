import logging
import os
from celery import shared_task, chain # noqa: F401
from config.settings import base

from kino.video.models import Media, Task
from kino.enums import StatusChoose
from kino.utils.download_video import download_video_from_s3
from kino.utils.record_video import record_video
from kino.utils.check_s3 import connection_to_s3


media_path = base.PATH_TO_MEDIA


# Пока что настроено без очередей

# @shared_task
def download_video(media_id):
    media = Media.objects.get(id=media_id)
    destination_path = os.path.join(media_path, "source", media.card.name)
    if not os.path.exists(destination_path):  # Проверяем, скачан ли файл
        if connection_to_s3():
            Task.objects.create(media=media, status=StatusChoose.processing)
            logging.info("Download started from S3")
            video_path = download_video_from_s3(media, destination_path)
        else:
            video_path = media.source_link
            logging.info("Download started from local machine")
            Task.objects.create(media=media, status=StatusChoose.processing)
            record_video(video_path, media)

# Потом доделать очереди

"""
@shared_task
def encode_video(video_path, media_id):
    record_video(video_path, media_id).delay()


@shared_task
def upload_video(video_path, media_id):
    upload_video_to_s3(video_path, media_id)
"""
