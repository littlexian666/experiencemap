from logger import logger
from starlette.middleware.cors import CORSMiddleware
import traceback
from pydantic import BaseModel
import time
import RedisHandler
import Constant
from main import app
import json


# 入参
class Req(BaseModel):
    # 模块
    module: str
    content: dict
class Req1(BaseModel):
    # 模块
    module: str


app.add_middleware(
    CORSMiddleware,
    # 允许跨域的源列表，例如 ["http://www.example.org"] 等等，["*"] 表示允许任何源
    allow_origins=["*"],
    # 跨域请求是否支持 cookie，默认是 False，如果为 True，allow_origins 必须为具体的源，不可以是 ["*"]
    allow_credentials=False,
    # 允许跨域请求的 HTTP 方法列表，默认是 ["GET"]
    allow_methods=["*"],
    # 允许跨域请求的 HTTP 请求头列表，默认是 []，可以使用 ["*"] 表示允许所有的请求头
    # 当然 Accept、Accept-Language、Content-Language 以及 Content-Type 总之被允许的
    allow_headers=["*"],
    # 可以被浏览器访问的响应头, 默认是 []，一般很少指定
    # expose_headers=["*"]
    # 设定浏览器缓存 CORS 响应的最长时间，单位是秒。默认为 600，一般也很少指定
    # max_age=1000
)


@app.post("/business/getContent")
async def get_content(req: Req1):
    start = time.time()
    logger.info(f'/business/getContent req content： {req}')
    module = req.module
    try:
        res_data = RedisHandler.get_all_from_z_set(Constant.business_key + module)

        res = []
        for data in res_data:
            data = json.loads(data)
            res.append(data)
        logger.info(f"res:{res}")
        logger.info(f"cost:{time.time() - start}")
        return {"code": "00000", "message": "success", "data": res}
    except Exception as e:
        logger.error(traceback.format_exc())
        return {"code": 500, "message": traceback.format_exc(), "data": "Error"}


#
@app.post("/business/getModuleList")
async def getModuleList():
    start = time.time()
    logger.info(f'/experience/getContent/getModuleList req')

    # todo: 校验参数
    try:
        res = []
        for key in Constant.module_to_name.keys():
            value = Constant.module_to_name.get(key)
            obj = {
                "module": key,
                "moduleName": value
            }
            res.append(obj)
        # todo: 实现

        logger.info(f"res:{res}")
        logger.info(f"cost:{time.time() - start}")

        return {"code": "00000", "message": "success", "data": res}
    except Exception as e:
        logger.error(traceback.format_exc())
        return {"code": 500, "message": traceback.format_exc(), "data": "Error"}


@app.post("/business/pushContent")
async def push_content(req: Req):
    start = time.time()
    logger.info(f'/business/pushContent req content： {req}')
    module = req.module
    content = req.content
    try:

        res_data = RedisHandler.get_all_from_z_set(Constant.business_key + module)

        for data in res_data:
            data = json.loads(data)
            if data['record_id'] == content['record_id']:
                return {"code": "00000", "message": "已经推送过了"}
        RedisHandler.set_data_to_z_set(Constant.business_key + module, content, time.time())
        return {"code": "00000", "message": "success"}
    except Exception as e:
        logger.error(traceback.format_exc())
        return {"code": 500, "message": traceback.format_exc(), "data": "Error"}

