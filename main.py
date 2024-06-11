from dotenv import load_dotenv
import os
from rich import print
from qiniu import Auth, put_file

load_dotenv()
access_key = os.getenv('QINIU_ACCESS_KEY')
secret_key = os.getenv('QINIU_SECRET_KEY')
q = Auth(access_key, secret_key)
bucket_name = os.getenv('QINIU_BUCKET_NAME')

cloud_filename = 'cloud.jpg'
local_filename = r'./temp/local.jpg'

token = q.upload_token(bucket_name, cloud_filename, 3600)
# ret, info = put_file(token, cloud_filename, local_filename)
#
# print(ret)
# print(info)
