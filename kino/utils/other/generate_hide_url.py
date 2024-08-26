from uuid import uuid4


def media_url_generate() -> str:
    return uuid4().hex


def upload_to_posters(instance, filename) -> str:
    ext = filename.split(".")[-1]
    filename = f"{uuid4().hex}.{ext}"
    return f"posters/{filename}"


def upload_to_serials(instance, filename) -> str:
    ext = filename.split(".")[-1]
    filename = f"{uuid4().hex}.{ext}"
    return f"photos_serials/{filename}"


def upload_to_films(instance, filename) -> str:
    ext = filename.split(".")[-1]
    filename = f"{uuid4().hex}.{ext}"
    return f"photos_films/{filename}"


def upload_to_s3(bucket_name, filename) -> str:
    ext = filename.split(".")[-1]
    filename = f"{uuid4().hex}.{ext}"
    return f"{bucket_name}/{filename}"
