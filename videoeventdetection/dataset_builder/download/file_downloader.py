import os
from urllib.parse import urlparse
from .s3 import download_s3_file


def download_file(url: str, target_file: str):
    if os.path.exists(target_file):
        return  # File already exists in the cache

    parsed = urlparse(url)

    if parsed.scheme == "s3":
        download_s3_file(parsed.netloc, parsed.path, target_file)
    else:
        raise ValueError(f"Unsupported url scheme: {parsed.scheme}")


