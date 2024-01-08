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
import requests
import json


def qa(content: str):
    # res = Score(1, "哈哈哈")
    req = {
        "model": "chatglm3-6b",
        "messages": [{
            "role": "system",
            "content": "你擅长做细腻的情感分析，你精通保险行业术语， 请帮我分析客户对话文本中的情绪和痛点，情绪打分1-5，分值越高用户情绪越好，痛点总结要简洁明了在10字以内。 返回的数据用json格式，情绪用emotion，痛点用pain。 示例 ：输入：这家保险好坑，承诺的优惠券领不了 输出： {\" emotion\":\"2\",\"pain\":\"优惠券领不了\"} ； 输入：这家保险出现快，我很喜欢 输出： {\" emotion\":\"5\",\"pain\":\"出险快\"} "
        }, {
            "role": "user",
            "content": content
        }],
        "stream": False,
        "max_tokens": 100,
        "temperature": 0.8,
        "top_p": 0.8
    }

    headers = {'content-type': 'application/json'}
    response = requests.post('http://36.137.226.16:11139/v1/chat/completions', data=json.dumps(req), headers=headers)
    print(response.status_code)
    print(response.json())
    res = response.json()
    choices = res.get('choices')[0]
    content = choices.get('message').get('content')
    content = json.loads(content)
    res = {'score': int(content.get('emotion')), 'summary': str(content.get('pain'))}
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
        res_data = qa(req.content)

        logger.info(f"res:{res_data}")
        logger.info(f"cost:{time.time() - start}")
        return {"code": "00000", "message": "success", "data": res_data}
    except Exception as e:
        logger.error(traceback.format_exc())
        return {"code": 500, "message": traceback.format_exc(), "data": "Error"}


# 模拟用户真实场景
@app.post("/user_qa")
async def user_qa(req: UserQaReq):
    start = time.time()
    logger.info(f'user_qa req content： {req}')
    ##todo:参数校验
    try:
        if req.flow_path not in Constant.flow_path:
            return {"code": "-1", "message": "无此流程"}
        # 暂定一个流程里只能有一个问答
        res_data = RedisHandler.get_all_from_z_set(Constant.user_data_key + req.user_id)
        exist_path = []
        if res_data:
            for data in res_data:
                data = json.loads(data)
                exist_path.append(data.get('flow_path'))
        if req.flow_path in exist_path:
            return {"code": "-2", "message": "该流程已有数据"}
        res_data = qa(req.content)
        record_id = RedisHandler.get_record_id()
        redis_data = Entity.ExperienceRecord(record_id, req.user_id, req.flow_path, req.scene, req.content, time.time())
        # 存qa记录
        RedisHandler.set_data_to_z_set(Constant.user_data_key + req.user_id, redis_data, time.time())
        RedisHandler.set_data_to_z_set(Constant.user_data_all_key, redis_data, time.time())
        # 存模型结果
        RedisHandler.hset(Constant.score_data_key, record_id, res_data)

        logger.info(f"cost:{time.time() - start}")
        return {"code": "00000", "message": "success"}
    except Exception as e:
        logger.error(traceback.format_exc())
        return {"code": 500, "message": traceback.format_exc(), "data": "Error"}
