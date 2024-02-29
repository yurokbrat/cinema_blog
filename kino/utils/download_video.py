import boto3


# скачивание файла с s3 с помощью boto3
def download_video_from_s3(source, destination_path):
    file_name = source.split("/")[-1]
    s3 = boto3.client("s3")
    s3.download_file("bucket_name", file_name, destination_path)
    return destination_path
