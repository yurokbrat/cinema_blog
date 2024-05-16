import logging
from pathlib import Path

from config import celery_app
from kino.enums import StatusChoose
from kino.utils.stages_of_video.upload import upload_video
from kino.video.models import Media, Task


def processing_video(  # noqa: PLR0913
    quality,
    output_directory,
    input_video,
    media,
    aspect_ratio,
    task_id,
):
    bitrate_params = {
        "360": {"video_bitrate": "1000k", "audio_bitrate": "128k"},
        "480": {"video_bitrate": "1800k", "audio_bitrate": "162k"},
        "720": {"video_bitrate": "3500k", "audio_bitrate": "220k"},
    }
    quality_width = round((quality * aspect_ratio) / 2) * 2
    vf_filter = f"scale={quality_width}:{quality}"
    output_file = Path(output_directory, f"{quality}.mp4")
    output_video = input_video.output(
        str(output_file),
        vf=vf_filter,
        r=23.976,
        **{"b:v": bitrate_params[str(quality)]["video_bitrate"], "b:a": bitrate_params[str(quality)]["audio_bitrate"]},
    ).overwrite_output()
    output_video.run()
    info_end_encode = f"{media.card.name} was converted to {quality}"
    logging.info(info_end_encode)
    load_video.delay(str(output_file), media.id, task_id)


@celery_app.task()
def load_video(output_file, media_id, task_id):
    media = Media.objects.get(id=media_id)
    task = Task.objects.get(id=task_id)
    try:
        upload_video(output_file, media)
        task.status = StatusChoose.completed
        task.save()
    except Exception:
        task.status = StatusChoose.failed
        task.save()
        logging.exception("Error during video uploading")
