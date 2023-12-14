##  调用模型的接口

import time

import Constant
import RedisHandler
from logger import logger
from pydantic import BaseModel
from Vo import Score
import traceback
from main import app
import Entity


def qa():
    res = Score(1, "哈哈哈")
    return res


# 入参
class Req(BaseModel):
    content: str  # 内容


# 入参
class UserQaReq(BaseModel):
    content: str  # 内容
    user_id: str  # 用户id
    flow_path: str  # 流程
    scene: str  # 收集场景


# 模拟问答-once
@app.post("/test_qa")
async def test_qa(req: Req):
    start = time.time()
    logger.info(f'test_qa req content： {req}')
    try:
        res_data = qa()

        logger.info(f"res:{res_data}")
        logger.info(f"cost:{time.time() - start}")
        return {"code": 200, "message": "success", "result": res_data}
    except Exception as e:
        logger.error(traceback.format_exc())
        return {"code": 500, "message": traceback.format_exc(), "result": "Error"}


# 模拟用户真实场景
@app.post("/user_qa")
async def user_qa(req: UserQaReq):
    start = time.time()
    logger.info(f'user_qa req content： {req}')
    ##todo:参数校验
    try:
        res_data = qa()
        record_id = RedisHandler.get_record_id()
        redis_data = Entity.ExperienceRecord(record_id, req.user_id, req.flow_path, req.scene, req.content, time.time())
        # 存qa记录
        RedisHandler.set_data_to_z_set(Constant.user_data_key + req.user_id, redis_data, time.time())
        RedisHandler.set_data_to_z_set(Constant.user_data_all_key, redis_data, time.time())
        # 存模型结果
        RedisHandler.hset(Constant.score_data_key, record_id, res_data)
        logger.info(f"cost:{time.time() - start}")
        return {"code": 200, "message": "success"}
    except Exception as e:
        logger.error(traceback.format_exc())
        return {"code": 500, "message": traceback.format_exc(), "result": "Error"}
