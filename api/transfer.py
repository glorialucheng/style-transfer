from PIL import Image
from fast_model import ffwd_to_img
from dotenv import load_dotenv
import os
from qiniu import Auth, put_file
from pydantic import BaseModel
from time import time

load_dotenv()
access_key = os.getenv('QINIU_ACCESS_KEY')
secret_key = os.getenv('QINIU_SECRET_KEY')
q = Auth(access_key, secret_key)
bucket_name = os.getenv('QINIU_BUCKET_NAME')
base_url = os.getenv('QINIU_BASE_URL')


class Result(BaseModel):
    status: str
    url: str
    data: str
    duration: str = None


# 压缩图片
def compress_image(image_path):
    im = Image.open(image_path)
    if image_path.endswith(".png"):
        im = im.convert('P')
    im.save(image_path, optimize=True)


def upload2qiniu(cloud_filename, local_filename):
    token = q.upload_token(bucket_name, cloud_filename, 3600)
    t1 = time()
    # ret, info = put_file(token, cloud_filename, local_filename)
    ret, info = put_file(token, cloud_filename, r'E:\project\style-transfer\temp\cloud.jpg')
    t2 = time()
    if info.status_code == 200:
        return os.path.join(base_url, cloud_filename)
    else:
        return ''


def transfer(image_path, image_name, result_image_path, result_image_name, ckpt_path):
    compress_image(os.path.join(image_path, image_name))
    t1 = time()
    ffwd_to_img(os.path.join(image_path, image_name), os.path.join(result_image_path, result_image_name), ckpt_path)
    t2 = time()
    url = upload2qiniu(result_image_name, os.path.join(result_image_path, result_image_name))
    t3 = time()
    if url != '':
        res = {'status': 200, 'url': url, 'transfer_duration': t2 - t1, 'upload_duration': t3 - t2}
    else:
        res = {'status': 400, 'url': url, 'transfer_duration': t2 - t1, 'upload_duration': t3 - t2}

    return res
