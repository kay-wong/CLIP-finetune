from concurrent import futures
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sys
from progress.bar import Bar
from PIL import Image
import time
import os

IMG_DIR_PATH = sys.argv[1] 
BUCKET_NAME = "my-bucket"

def resize_images(file_name):
    download_path = Path(IMG_DIR_PATH + "/" + file_name)
    resize_image(download_path)
    return "Success"

def resize_parallel_multithreading(imgs_to_resize):

    # Dispatch work tasks 
    with ThreadPoolExecutor(max_workers=8) as executor:
        future_to_key = {executor.submit(resize_images, key): key for key in imgs_to_resize}

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
# python aws-batch-download.py train_data ./train_data_resize
if __name__ == "__main__":
    imgs_to_resize = os.listdir(IMG_DIR_PATH)

    start = time.time()
    bar = Bar('Processing', max=len(imgs_to_resize))
    for key, result in resize_parallel_multithreading(imgs_to_resize):
        bar.next()
    bar.finish()
    end = time.time()
    print("Total runtime: {}".format(end-start))