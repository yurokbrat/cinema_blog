from config.settings.base import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


def connection_to_s3():
    return AWS_ACCESS_KEY_ID != "" and AWS_SECRET_ACCESS_KEY != ""



