# for redis
business_key = "business_key:"  # 业务方数据 如 business_key:hsh

user_data_key = "user_data:"  # qa数据 如 user_data:123
user_data_all_key = "user_data_all"  # qa数据-all

score_data_key = "score_data"  # 分数 map  recordid:value

record_id_key = "record_id"  # 唯一id

flow_path = ["触达", "报价", "支付", "服务使用", "报案", "评价"]


module_to_name = {
    "seat": "坐席",
    "service": "服务",
    "claim": "理赔",
    "pay": "收银台",
}