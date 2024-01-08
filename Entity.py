# 比如 用户甲在流程A的场景1中提交了反馈内容xxx，产生了一条记录
class ExperienceRecord:
    def __init__(self, record_id, user_id, flow_path, scene, content, create_time):
        self.record_id = record_id  # 记录id
        self.user_id = user_id  # 用户id
        self.flow_path = flow_path  # 流程
        self.scene = scene  # 收集场景
        self.content = content  # 收集内容
        self.create_time = create_time  # 收集时间


# 模型的结果
class Score:
    def __init__(self, record_id, score, summary, create_time):
        self.record_id = record_id  # 记录id
        self.score = score  # 评分
        self.summary = summary  # 摘要
        self.create_time = create_time  # 输出时间


# 推送给业务方的内容
#{"record_id":"1","user_id":"111","flow_path":"附近的卡上了","scene":"fjdla","content":"reqvc","score":"1","summary":"fd","create_time":"fda"}
class PushContent:
    def __init__(self, module, record_id, user_id, flow_path, scene, content, score, summary, create_time):
        self.module = module  # 模块
        self.record_id = record_id  # 记录id
        self.user_id = user_id  # 用户id
        self.flow_path = flow_path  # 流程
        self.scene = scene  # 收集场景
        self.content = content  # 收集内容
        self.create_time = create_time  # 收集时间
        self.score = score  # 评分
        self.summary = summary  # 摘要
