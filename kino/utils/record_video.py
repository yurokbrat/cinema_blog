import logging
import ffmpeg
from pathlib import Path
from kino.enums import StatusChoose
from kino.video.models import Task
from config.settings import base

media_path = base.PATH_TO_MEDIA


# кодировка видео в разные качества
def record_video(input_file, media_id):
    from kino.video.tasks import save_or_upload_quality
    from kino.video.models import Media
    media = Media.objects.get(id=media_id)
    try:
        logging.info(f"Starting encode for {input_file}")
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

        output_files = []

        for quality in qualities:
            quality_width = round((quality * aspect_ratio) / 2) * 2
            vf_filter = f"scale={quality_width}:{quality}"
            output_directory = Path(media_path) / "quality" / f"{media.card.name}"
            output_directory.mkdir(parents=True, exist_ok=True)
            logging.info(f"out directory - {output_directory}")
            output_file = f"{output_directory}\\{media.card.name}_{quality}.mp4"
            logging.info(f"output_file - {output_file}")
            output_video = (
                input_video
                .output(output_file,
                        vf=vf_filter,
                        r=23.976,
                        **{"b:v": bitrate_params[str(quality)]["video_bitrate"],
                           "b:a": bitrate_params[str(quality)]["audio_bitrate"]})
                .overwrite_output()
            )
            output_video.run()
            output_files.append(output_file)
            logging.info(f"{media.card.name} was converted to {quality}")
            save_or_upload_quality.delay(output_file, media.id)
        Task.objects.filter(media=media).update(status=StatusChoose.completed)
    except Exception:
        Task.objects.filter(media=media).update(status=StatusChoose.failed)
        logging.exception("Error during video encoding")
