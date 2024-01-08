# encoding=utf-8
from fastapi import FastAPI
import uvicorn


app = FastAPI()



# 服务启动方法
if __name__ == '__main__':
    import Model
    import Business
    import ExperiencePage
    uvicorn.run('main:app', host='0.0.0.0', port=11133)
