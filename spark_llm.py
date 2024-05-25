import os
import json
from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
from typing import List, Optional

# 使用环境变量读取敏感信息
SPARKAI_URL = 'wss://spark-api.xf-yun.com/v3.5/chat'
SPARKAI_APP_ID = os.getenv('SPARKAI_APP_ID', 'bc037f86')
SPARKAI_API_SECRET = os.getenv('SPARKAI_API_SECRET', 'ZWRmM2U4NTVhYmFlYzZlYTQ2NWUzOTNj')
SPARKAI_API_KEY = os.getenv('SPARKAI_API_KEY', '669bec0d5cefb03396851d2b93080fc5')
SPARKAI_DOMAIN = 'generalv3.5'


def _build_prompt(subject: str, question_type: str, difficulty: int, num_questions: int, score: int,
                  knowledge: Optional[str] = None, tags: Optional[List[str]] = None) -> str:
    """
    构建生成题目的prompt字符串
    """
    # 生成题目数据
    data = {
        "题型": question_type,
        "题干": f"以下哪一项不是导致{subject}的原因？",
        "正确答案": "D",
        "答案解析": "这是一道示例题目的答案解析。",
        "分值": score,
        "难度系数": difficulty,
        "知识点": knowledge,
        "标签": tags if tags else [],
        "A": f"选项A_{subject}",
        "B": f"选项B_{subject}",
        "C": f"选项C_{subject}",
        "D": f"选项D_{subject}"
    }
    json_str = json.dumps(data, ensure_ascii=False, indent=4)
    prompt_pre = f"帮我生成{num_questions}道{subject}学科的题目，题型为{question_type}，分值为{score}，难度系数为{difficulty}"
    if knowledge:
        prompt_pre += f", 知识点为{knowledge}"
    if tags:
        prompt_pre += f", 标签为{'、'.join(tags)}"
    prompt_end = (
        f"{prompt_pre}",
        "其中难度系数越大，难度越高，总共有1、2、3、4、5这5个档",
        "最终结果以json格式输出，包括“题型”、“题干”、“正确答案”、“答案解析”、“分值”、“难度系数”、“知识点”、“标签”以及A、B、C、D选项",
        "题目示例：",
        f"{json_str}"
        f"其中填空题有几个空就用几个_代替"
    )
    return prompt_end


def build_prompt(subject: str, question_type: str, difficulty: int, num_questions: int, score: int,
                 knowledge: Optional[str] = None, tags: Optional[List[str]] = None) -> str:
    """
    构建生成题目的prompt字符串
    """
    # 生成题目数据
    data = {
        "题型": question_type,
        "题干": f"以下哪一项不是导致{subject}的原因？",
        "正确答案": "D",
        "答案解析": "这是一道示例题目的答案解析。",
        "分值": score,
        "难度系数": difficulty,
        "知识点": knowledge,
        "标签": tags if tags else [],
        "A": f"选项A_{subject}",
        "B": f"选项B_{subject}",
        "C": f"选项C_{subject}",
        "D": f"选项D_{subject}"
    }
    json_str = json.dumps(data, ensure_ascii=False, indent=4)
    prompt_pre = f"帮我生成{num_questions}道{subject}学科的题目，题型为{question_type}，分值为{score}，难度系数为{difficulty}"
    if knowledge:
        prompt_pre += f", 知识点为{knowledge}"
    if tags:
        prompt_pre += f", 标签为{'、'.join(tags)}"
    prompt_end = (
        f"{prompt_pre}，其中难度系数越大，难度越高，总共有1、2、3、4、5这5个档，最终结果以json格式输出，包括“题型”、“题干”、“正确答案”、“答案解析”、“分值”、“难度系数”、“知识点”、“标签”以及A、B、C、D选项，最终的json输出的key值分别为题型、题干、正确答案、答案解析、分值、难度系数、知识点、标签、A、B、C、D，有多个题目时，将json整合成一个使用[]包含的标准的json，其中填空题有几个空就用几个_代替"
    )
    return prompt_end


def generate_question(subject: str, question_type: str, difficulty: int, num_questions: int, score: int,
                      knowledge: Optional[str] = None, tags: Optional[List[str]] = None) -> str:
    """
    生成题目
    """
    # 参数校验可以进一步增强，这里仅示例基本检查
    if not isinstance(num_questions, int) or num_questions <= 0 or num_questions > 100:  # 限制最大值为100
        raise ValueError("num_questions 必须是1到100之间的正整数")
    if not subject or not question_type:
        raise ValueError("subject和question_type不能为空")
    if not 1 <= difficulty <= 5:
        raise ValueError("difficulty 必须是1到5之间的整数")
    if score < 0:
        raise ValueError("score 必须是非负整数")

    try:
        prompt_latest = _build_prompt(subject, question_type, difficulty, num_questions, score, knowledge, tags)
        return prompt_latest
    except Exception as e:
        print(f"生成题目时发生错误：{e}")
        return ""
def generate_content(prompt: str):
    spark = ChatSparkLLM(
        spark_api_url=SPARKAI_URL,
        spark_app_id=SPARKAI_APP_ID,
        spark_api_key=SPARKAI_API_KEY,
        spark_api_secret=SPARKAI_API_SECRET,
        spark_llm_domain=SPARKAI_DOMAIN,
        streaming=False,
    )
    messages = [ChatMessage(
        role="user",
        content=prompt
        # "帮我生成5道数值分析学科的题目，题型为多选题，分值为2，难度系数为3, 知识点为拉格朗日插值法', '其中难度系数越大，难度越高，总共有1、2、3、4、5这5个档', "
        #         "'最终结果以json格式输出，包括“题型”、“题干”、“正确答案”、“答案解析”、“分值”、“难度系数”、“知识点”、“标签”以及A、B、C、D选项', "
        #         "'最终的json输出的key值分别为题型、题干、正确答案、答案解析、分值、难度系数、知识点、标签、A、B、C、D', '其中填空题有几个空就用几个_代替'"
    )]
    handler = ChunkPrintHandler()
    try:
        a = spark.generate([messages], callbacks=[handler])
        print(a)
    except Exception as e:
        print(f"与Spark AI通信时发生错误：{e}")


if __name__ == '__main__':
    prompt = build_prompt("语文", "单选题", 3, 2, 2)
    prompt2 = generate_question("数值分析", "多选题", 3, 5, 2, "拉格朗日插值法")
    prompt = prompt.strip('()')
    # prompt2 = prompt2.strip('()')
    # print(prompt)
    # print(prompt2)
    subject = "数值分析"
    query = f"帮我出一道{subject}单选题"
    generate_content(prompt)