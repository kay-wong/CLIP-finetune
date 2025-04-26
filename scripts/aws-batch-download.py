import boto3.session
from botocore.config import Config
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sys
from progress.bar import Bar
from PIL import Image
import time
import os

KEYS_FILE = sys.argv[1] 
LOCAL_DOWNLOAD_PATH = sys.argv[2] 
BUCKET_NAME = "my-bucket"

def download_object(s3_client, file_name):
    download_path = Path(LOCAL_DOWNLOAD_PATH + "/" + file_name  + ".jpg")
    s3_client.download_file(
        BUCKET_NAME,
        file_name + "/raw",
        str(download_path)
    )
    resize_image(download_path)
    return "Success"

def download_parallel_multithreading(keys_to_download):
    # Create a session and use it to make our client
    session = boto3.session.Session()
    s3_client = session.client("s3")

    # Dispatch work tasks with our s3_client
    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_key = {executor.submit(download_object, s3_client, key): key for key in keys_to_download}

        for future in futures.as_completed(future_to_key):
            key = future_to_key[future]
            exception = future.exception()

            if not exception:
                yield key, future.result()
            else:
                yield key, exception

def resize_image(filename):
    with Image.open(filename) as img:
        if img.mode not in ['RGB']:
            img = img.convert('RGB')
        maxsize = (640, 640)
        img.thumbnail(maxsize)
        img.save(filename, "JPEG")


# Usage:
# python aws-batch-download.py sample_data/sample_keys.tsv ./tst_out
if __name__ == "__main__":
    with open(KEYS_FILE) as f:
        keys_to_download = f.read().splitlines() 

    start = time.time()
    bar = Bar('Processing', max=len(keys_to_download))
    for key, result in download_parallel_multithreading(keys_to_download):
        bar.next()
    bar.finish()
    end = time.time()
    print("Total runtime: {}".format(end-start))
