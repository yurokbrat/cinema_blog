from pathlib import Path

import ffmpeg


def check_quality_video(file: Path) -> tuple[int, int] | None:
    ffmpeg.input(file)
    info = ffmpeg.probe(file)
    if video_stream := next(
        stream for stream in info["streams"] if stream["codec_type"] == "video"
    ):
        width = int(video_stream["width"])
        height = int(video_stream["height"])
        return width, height
    return None
