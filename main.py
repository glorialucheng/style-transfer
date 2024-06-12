from dotenv import load_dotenv
import os
from rich import print
from qiniu import Auth, put_file

load_dotenv()
access_key = os.getenv('QINIU_ACCESS_KEY')
secret_key = os.getenv('QINIU_SECRET_KEY')
q = Auth(access_key, secret_key)
bucket_name = os.getenv('QINIU_BUCKET_NAME')

# from api import transfer
cloud_filename = 'cloud.jpg'
local_filename = r'./temp/cloud.jpg'
# res = transfer('./temp', 'local.jpg', './temp', 'cloud.jpg', r'./fast_model/ckpt/scream.ckpt')
# print(res)
token = q.upload_token(bucket_name, cloud_filename, 3600)
ret, info = put_file(token, cloud_filename, local_filename)

print(ret)
print(info)

# {'hash': 'FvPmOHZjErcskLdaWC7A9wbzF_08', 'key': 'cloud.jpg'}
# _ResponseInfo__response:<Response [200]>, exception:None, status_code:200,
# text_body:{"hash":"FvPmOHZjErcskLdaWC7A9wbzF_08","key":"cloud.jpg"},
# req_id:D2IAAADjdvp_LtgX, x_log:X-Log
