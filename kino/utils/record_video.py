import logging
import re
import ffmpeg
from pathlib import Path
from django.conf import settings

from kino.enums import StatusChoose
from kino.video.models import Task, Media
from kino.utils import upload_video

media_path = settings.PATH_TO_MEDIA


# Record video in different qualities
def record_video(input_file, media_id):
    media = Media.objects.get(id=media_id)
    try:
        logging.info(f"АААААААААmedia_path = {media_path}")
        info_start_encode = f"Starting encode for {input_file}"
        logging.info(info_start_encode)
        input_video = ffmpeg.input(input_file)
        info = ffmpeg.probe(input_file)
        video_stream = next((stream for stream in info["streams"] if stream["codec_type"] == "video"), None)
        width = int(video_stream["width"])
        height = int(video_stream["height"])
        aspect_ratio = width / height

        qualities = [360, 480, 720]

        bitrate_params = {
            "360": {"video_bitrate": "1000k", "audio_bitrate": "128k"},
            "480": {"video_bitrate": "1800k", "audio_bitrate": "162k"},
            "720": {"video_bitrate": "3500k", "audio_bitrate": "220k"},
        }

        for quality in qualities:
            quality_width = round((quality * aspect_ratio) / 2) * 2
            vf_filter = f"scale={quality_width}:{quality}"
            directory_name = re.sub(r'[:"/\\|?*]', '', media.card.name)
            output_directory = Path(media_path, "quality", directory_name)
            output_directory.mkdir(parents=True, exist_ok=True)
            output_file = Path(output_directory, f"{quality}.mp4")
            output_video = (
                input_video
                .output(str(output_file),
                        vf=vf_filter,
                        r=23.976,
                        **{"b:v": bitrate_params[str(quality)]["video_bitrate"],
                           "b:a": bitrate_params[str(quality)]["audio_bitrate"]})
                .overwrite_output()
            )
            output_video.run()
            info_end_encode = f"{media.card.name} was converted to {quality}"
            logging.info(info_end_encode)
            upload_video(output_file, media)
        Task.objects.filter(media=media).update(status=StatusChoose.completed)
    except Exception:
        Task.objects.filter(media=media).update(status=StatusChoose.failed)
        logging.exception("Error during video encoding")
