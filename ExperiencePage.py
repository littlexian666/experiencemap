# encoding=utf-8
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


# ["触达", "报价", "支付", "服务使用", "报案", "评价"]
path_to_module = {
    "触达": "seat",
    "报价": "seat",
    "支付": "service",
    "服务使用": "service",
    "报案": "claim",
    "评价": "seat"
}


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

        return {"code": "00000", "message": "success", "data": result_list}
    except Exception as e:
        logger.error(traceback.format_exc())
        return {"code": 500, "message": traceback.format_exc(), "data": "Error"}


# 获取用户的列表
@app.post("/experience/getUserList")
async def get_content_get_user_list():
    start = time.time()
    logger.info(f'/experience/getContent/get_user_list req')

    # todo: 校验参数
    try:
        # todo: 实现
        res_data = ["111", "222", "333"]
        logger.info(f"res:{res_data}")
        logger.info(f"cost:{time.time() - start}")

        return {"code": "00000", "message": "success", "data": res_data}
    except Exception as e:
        logger.error(traceback.format_exc())
        return {"code": 500, "message": traceback.format_exc(), "data": "Error"}


# 获取记录 传入userid是个人 不传入是整体
@app.post("/experience/getContent")
async def get_content(req: Req_Personal):
    start = time.time()
    logger.info(f'/experience/getContent/personal req content： {req}')
    user_id = req.user_id
    # todo: 校验参数
    try:
        result = []
        ## 个人的获取
        if user_id != '':
            res_data = RedisHandler.get_all_from_z_set(Constant.user_data_key + user_id)
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
                            data['module'] = path_to_module.get(data['flow_path']) or 'seat'
                            data['moduleName'] = Constant.module_to_name.get(data['module']) or '坐席'
                            result_list.append(data)
            result = result_list
        else:
            res_data = RedisHandler.get_all_from_z_set(Constant.user_data_all_key)
            # result = {}
            result = []
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
                groups = {

                }
                for data in result_list:
                    group = groups.get(data['flow_path']) or []
                    if not group:
                        groups[data['flow_path']] = [data]
                    else:
                        group.append(data)
                # groups = itertools.groupby(result_list, lambda x: x['flow_path'])
                for key in groups.keys():
                    group_list = groups.get(key)
                    logger.info(f'group_list： {group_list}')
                    score_list = [int(item['score']) for item in group_list]
                    avg_score = sum(score_list) / len(score_list)
                    summary_list = [item['summary'] for item in group_list]
                    scene_list = [item['scene'] for item in group_list]
                    scene = []
                    for s in scene_list:
                        if s not in scene:
                            scene.append(s)
                    module = path_to_module.get(key) or 'seat'
                    module_name = Constant.module_to_name.get(module) or '坐席'
                    result.append(ExperienceResult(key, avg_score, summary_list, ','.join(scene), module_name))

        logger.info(f"res:{result}")
        logger.info(f"cost:{time.time() - start}")

        return {"code": "00000", "message": "success", "data": result}
    except Exception as e:
        logger.error(traceback.format_exc())
        return {"code": 500, "message": traceback.format_exc(), "data": "Error"}
