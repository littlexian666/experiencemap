# 单人

class ExperienceResult:
    def __init__(self, flow_path, score, summary):
        self.flow_path = flow_path  # 流程
        self.avg_score = score  # 评分
        self.summary_list = summary  # 摘要


class Score:
    def __init__(self, score, summary):
        self.score = score  # 评分
        self.summary = summary  # 摘要
