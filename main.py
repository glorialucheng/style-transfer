from api import transfer
from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def home():
    return 'Hello World!'


@app.get("/transfer")
def style_transfer():
    res = transfer('./temp', 'local.jpg', './temp', 'cloud.jpg', r'./fast_model/ckpt/scream.ckpt')
    return res


if __name__ == '__main__':
    uvicorn.run(app='main:app', host='127.0.0.1', port=8000, reload=True)
