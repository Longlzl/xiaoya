import os
import json
import google.generativeai as genai
from typing import List, Optional

# 建议将配置信息单独存放在环境变量或配置文件中，这里仍然采用环境变量示例
os.environ["HTTPS_PROXY"] = "http://127.0.0.1:7890"
os.environ["HTTP_PROXY"] = "http://127.0.0.1:7890"
os.environ["https_proxy"] = "http://127.0.0.1:7890"
os.environ["http_proxy"] = "http://127.0.0.1:7890"
# API Key 鉴权也建议从安全的配置源获取
genai.configure(api_key="AIzaSyBC28DFuinhTiw2xBUOj4DaCT8Tjf6ZG7I")

class QuestionGenerator:
    def __init__(self):
        pass

    def _build_prompt(self, subject: str, question_type: str, difficulty: int, num_questions: int, score: int,
                      knowledge: Optional[str] = None, tags: Optional[List[str]] = None) -> str:
        """
        构建生成题目的prompt字符串
        """
        prompt_pre = f"帮我生成{num_questions}道{subject}学科的题目，题型为{question_type}，分值为{score}，难度系数为{difficulty}"
        if knowledge:
            prompt_pre += f", 知识点为{knowledge}"
        if tags:
            prompt_pre += f", 标签为{'、'.join(tags)}"
        prompt_parts = [
            prompt_pre,
            "其中难度系数越大，难度越高，总共有1、2、3、4、5这5个档",
            "最终结果以json格式输出，包括“题型”、“题干”、“正确答案”、“答案解析”、“分值”、“难度系数”、“知识点”、“标签”以及A、B、C、D选项",
            "题目示例："
        ]
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
        prompt_parts.append(json_str)
        return "\n".join(prompt_parts)

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

        # 对subject和question_type等进行一定的校验或清理，这里略去具体实现

        prompt = self._build_prompt(subject, question_type, difficulty, num_questions, score, knowledge, tags)
        return prompt

    def generate_content(self, prompt: str):
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            return response.text
        except genai.errors.GenerativeAIError as e:
            # 对genai库抛出的特定异常进行捕获和处理
            print(f"生成内容时发生错误: {e}")
            return ""
        except Exception as e:
            # 捕获其他不可预见的异常
            print(f"生成内容时发生不可预知的错误: {e}")
            return ""

# # 示例用法
# question_generator = QuestionGenerator()
# prompt = question_generator.generate_question("历史", "选择题", 2, 5, 2, "法国大革命", ["法国历史"])
# content = question_generator._generate_content(prompt)
# print(content)
