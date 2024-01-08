# 单人

class ExperienceResult:
    def __init__(self, flow_path, score, summary, scene_list, moduleName):
        self.flow_path = flow_path  # 流程
        self.score = score  # 评分
        self.scene = scene_list  # 收集场景
        self.summary_list = summary  # 摘要
        self.moduleName = moduleName  # 模块


class Score:
    def __init__(self, score, summary):
        self.score = score  # 评分
        self.summary = summary  # 摘要
