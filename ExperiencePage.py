from logger import logger
import traceback
from pydantic import BaseModel
import time
import RedisHandler
import Constant
from Vo import ExperienceResult
from main import app
import itertools
import json

# 入参 --个人
class Req_Personal(BaseModel):
    user_id: str  # 用户id


# 入参 -- 整体
class Req_all(BaseModel):
    # 模块
    user_id: str


# 按照记录的维度
@app.post("/experience/getContent/each")
async def get_content_each():
    start = time.time()
    logger.info(f'/experience/getContent/each req ')
    # 增加分页
    # todo: 校验参数
    try:
        res_data = RedisHandler.get_all_from_z_set(Constant.user_data_all_key)
        result_list = []
        if res_data:
            for data in res_data:
                data = json.loads(data)
                record_id = data.get('record_id') or 0
                if record_id != 0:
                    model_result = RedisHandler.hget(Constant.score_data_key, record_id)
                    if model_result:
                        model_result = json.loads(model_result)
                        data['score'] = model_result['score']
                        data['summary'] = model_result['summary']
                        result_list.append(data)
        logger.info(f"res:{result_list}")
        logger.info(f"cost:{time.time() - start}")

        return {"code": 200, "message": "success", "result": result_list}
    except Exception as e:
        logger.error(traceback.format_exc())
        return {"code": 500, "message": traceback.format_exc(), "result": "Error"}


# 获取用户的列表
@app.post("/experience/getContent/get_user_list")
async def get_content_get_user_list(req: Req_Personal):
    start = time.time()
    logger.info(f'/experience/getContent/get_user_list req content： {req}')
    user_id = req.user_id
    # todo: 校验参数
    try:
        # todo: 实现
        res_data = []
        logger.info(f"res:{res_data}")
        logger.info(f"cost:{time.time() - start}")

        return {"code": 200, "message": "success", "result": res_data}
    except Exception as e:
        logger.error(traceback.format_exc())
        return {"code": 500, "message": traceback.format_exc(), "result": "Error"}


# 获取记录 传入userid是个人 不传入是整体
@app.post("/experience/getContent")
async def get_content(req: Req_Personal):
    start = time.time()
    logger.info(f'/experience/getContent/personal req content： {req}')
    user_id = req.user_id
    # todo: 校验参数
    try:
        if user_id != '':
            res_data = RedisHandler.get_all_from_z_set(Constant.user_data_key + user_id)
        else:
            res_data = RedisHandler.get_all_from_z_set(Constant.user_data_all_key)

        result = {}
        result_list = []
        # 以 flow_path groupBy
        if res_data:
            for data in res_data:
                data = json.loads(data)
                record_id = data.get('record_id') or 0
                if record_id != 0:
                    model_result = RedisHandler.hget(Constant.score_data_key, record_id)
                    if model_result:
                        model_result = json.loads(model_result)
                        data['score'] = model_result['score']
                        data['summary'] = model_result['summary']
                        result_list.append(data)
            groups = itertools.groupby(result_list, lambda x: x['flow_path'])
            for key, group in groups:
                group_list = list(group)
                score_list = [item['score'] for item in group_list]
                avg_score = sum(score_list)/len(score_list)
                summary_list = [item['summary'] for item in group_list]
                result[key] = ExperienceResult(key, avg_score, summary_list)
        logger.info(f"res:{result}")
        logger.info(f"cost:{time.time() - start}")

        return {"code": 200, "message": "success", "result": result}
    except Exception as e:
        logger.error(traceback.format_exc())
        return {"code": 500, "message": traceback.format_exc(), "result": "Error"}
