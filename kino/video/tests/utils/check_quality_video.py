import ffmpeg


def check_quality_video(file):
    ffmpeg.input(file)
    info = ffmpeg.probe(file)
    video_stream = next(
        (stream for stream in info["streams"] if stream["codec_type"] == "video"),
        None,
    )
    width = int(video_stream["width"])
    height = int(video_stream["height"])
    return width, height
