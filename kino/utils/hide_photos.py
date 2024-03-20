from pathlib import Path
from uuid import uuid4


def rename_file(path):
    def wrapper(instance, filename):
        ext = filename.split(".")[-1]
        filename = f"{uuid4().hex}.{ext}"
        return Path(path, filename)
    return wrapper
