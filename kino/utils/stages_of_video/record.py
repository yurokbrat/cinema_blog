import logging
from pathlib import Path

import ffmpeg
from django.conf import settings

from kino.enums import StatusChoose
from kino.utils.other.create_folder import get_media_folders
from kino.utils.stages_of_video.encoding import processing_video
from kino.video.models import Task, Media

media_path = settings.PATH_TO_MEDIA


# Record video in different qualities
def record_video(input_file, media_id, task_id):
    media = Media.objects.get(id=media_id)
    task = Task.objects.get(id=task_id)
    try:
        input_video = ffmpeg.input(input_file)
        info = ffmpeg.probe(input_file)
        video_stream = next((stream for stream in info["streams"] if stream["codec_type"] == "video"), None)
        width = int(video_stream["width"])
        height = int(video_stream["height"])
        aspect_ratio = width / height
        qualities = [360, 480, 720]

        directory_name, content_type_folder = get_media_folders(media)
        output_directory = Path(
            media_path,
            "quality",
            content_type_folder,
            directory_name,
        )
        output_directory.mkdir(parents=True, exist_ok=True)
        info_start_encode = f"Starting encode to {output_directory}"
        logging.info(info_start_encode)

        for quality in qualities:
            processing_video(
                quality,
                output_directory,
                input_video,
                media,
                aspect_ratio,
                task_id,
            )

    except Exception:
        task.status = StatusChoose.failed
        task.save()
        logging.exception("Error during video encoding")
