import os
import json
import google.generativeai as genai
from typing import List, Optional
def _build_prompt(self, subject: str, question_type: str, difficulty: int, num_questions: int, score: int,
                  knowledge: Optional[str] = None, tags: Optional[List[str]] = None) -> str:
    """
    构建生成题目的prompt字符串
    """
    data = {
        "题型": "选择题",
        "题干": "以下哪一项不是导致法国大革命爆发的主要原因？",
        "正确答案": "D",
        "答案解析": "宗教改革与法国大革命的爆发没有直接关系。",
        "分值": 2,
        "难度系数": 2,
        "知识点": "法国大革命",
        "标签": "法国历史",
        "A": "专制君主制",
        "B": "社会等级制度",
        "C": "经济危机",
        "D": "宗教改革"
    }
    json_str = json.dumps(data, ensure_ascii=False, indent=4)
    prompt_pre = f"帮我生成{num_questions}道{subject}学科的题目，题型为{question_type}，分值为{score}，难度系数为{difficulty}"
    if knowledge:
        prompt_pre += f", 知识点为{knowledge}"
    if tags:
        prompt_pre += f", 标签为{'、'.join(tags)}"
    prompt = (
        f"{prompt_pre}",
        "其中难度系数越大，难度越高，总共有1、2、3、4、5这5个档",
        "最终结果以json格式输出，包括“题型”、“题干”、“正确答案”、“答案解析”、“分值”、“难度系数”、“知识点”、“标签”以及A、B、C、D选项",
        "题目示例：",
        f"{json_str}"
        f"其中填空题有几个空就用几个_代替"
    )
    return prompt

def generate_question(self, subject: str, question_type: str, difficulty: int, num_questions: int, score: int,
                      knowledge: Optional[str] = None, tags: Optional[List[str]] = None) -> str:
    """
    生成题目
    """
    # 参数校验可以进一步增强，这里仅示例基本检查
    if not isinstance(num_questions, int) or num_questions <= 0:
        raise ValueError("num_questions 必须是正整数")
    if not 1 <= difficulty <= 5:
        raise ValueError("difficulty 必须是1到5之间的整数")
    if score < 0:
        raise ValueError("score 必须是非负整数")

    prompt = self._build_prompt(subject, question_type, difficulty, num_questions, score, knowledge, tags)
    return prompt

def _generate_content(self, prompt: str):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"生成内容时发生错误: {e}")
        return ""