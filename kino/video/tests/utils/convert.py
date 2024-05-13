from pathlib import Path

import ffmpeg
from django.conf import settings

from kino.utils.stages_of_video.encoding import processing_video


def coding_video(media, task, quality, aspect_ratio):
    test_output_directory = Path(settings.PATH_TO_MEDIA, "tests", media.card.name)
    test_output_directory.mkdir(parents=True, exist_ok=True)
    test_video_path = ffmpeg.input(Path(f"{settings.PATH_TO_MEDIA}/source/films/try2241/Night_city_cut.mp4"))
    processing_video(
        quality,
        test_output_directory,
        test_video_path,
        media,
        aspect_ratio,
        task.id,
    )
