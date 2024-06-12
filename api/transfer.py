from PIL import Image
from fast_model import ffwd_to_img
from dotenv import load_dotenv
import os
from qiniu import Auth, put_file

load_dotenv()
access_key = os.getenv('QINIU_ACCESS_KEY')
secret_key = os.getenv('QINIU_SECRET_KEY')
q = Auth(access_key, secret_key)
bucket_name = os.getenv('QINIU_BUCKET_NAME')

# 压缩图片
def compress_image(image_path):
    im = Image.open(image_path)
    if image_path.endswith(".png"):
        im = im.convert('P')
    im.save(image_path, optimize=True)


def upload2qiniu(cloud_filename, local_filename):
    token = q.upload_token(bucket_name, cloud_filename, 3600)
    ret, info = put_file(token, cloud_filename, local_filename)


def transfer(image_path, result_image_path, ckpt_path):
    compress_image(image_path)
    ffwd_to_img(image_path, result_image_path, ckpt_path)
