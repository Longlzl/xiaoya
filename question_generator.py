import json
from io import StringIO

# from main import QuestionGenerator
from typing import List, Optional
import xlwings as xw
from spark_llm import build_prompt
from spark_llm import generate_content
import sys
from gemini_llm import _build_prompt
from gemini_llm import _generate_content

def generate_and_write_to_excel2(subject: str, question_type: str, difficulty: int, num_questions: int, score: int,
                                 # knowledge: Optional[str], tags: Optional[List[str]], excel_template: str,
                                 knowledge: Optional[str], tags: Optional[List[str]],
                                 output_filename: str) -> List[dict]:
    prompt = build_prompt(subject, question_type, difficulty, num_questions, score, knowledge, tags)

    original_stdout = sys.stdout
    output = StringIO()
    sys.stdout = output

    generate_content(prompt)

    sys.stdout = original_stdout
    response = output.getvalue()
    response_start = response.split('json')[1]
    response_end = response_start.split('message')[0]
    # 去除额外的反斜杠和转义字符
    response_text = response_end.replace('\\\\', '').replace('\\n', '\n').replace('\\"', '"')

    # 提取和处理JSON数据
    json_start = response_text.find('[')
    json_end = response_text.rfind(']')
    if json_start == -1 or json_end == -1:
        raise ValueError("无法找到有效的JSON数据")
    json_data_str = response_text[json_start:json_end + 1]
    questions = json.loads(json_data_str)

    # 写入Excel文件
    app = xw.App(visible=False)
    # wb = app.books.open(excel_template)
    wb = app.books.open('小雅导入题目模板v2.1.2200.xlsx')
    sht = wb.sheets[0]

    start_row = 4  # 假设从第10行开始追加数据
    current_row = start_row
    for row_data in questions:
        for col, value in enumerate(row_data.values()):
            sht.cells(current_row, col + 1).value = value
        current_row += 1

    new_filename = output_filename
    wb.save(new_filename)
    wb.close()
    app.quit()

    return questions


def generate_and_write_to_excel1(subject: str, question_type: str, difficulty: int, num_questions: int, score: int,
                                 knowledge: Optional[str], tags: Optional[List[str]],
                                 output_filename: str) -> List[dict]:
    prompt = _build_prompt(subject, question_type, difficulty, num_questions, score, knowledge, tags)
    response_text = _generate_content(prompt)

    # 提取和处理JSON数据
    json_start = response_text.find('[')
    json_end = response_text.rfind(']')
    if json_start == -1 or json_end == -1:
        raise ValueError("无法找到有效的JSON数据")
    json_data_str = response_text[json_start:json_end + 1]
    questions = json.loads(json_data_str)

    # 写入Excel文件
    app = xw.App(visible=False)
    wb = app.books.open('小雅导入题目模板v2.1.2200.xlsx')
    sht = wb.sheets[0]

    start_row = 4  # 假设从第10行开始追加数据
    current_row = start_row
    for row_data in questions:
        for col, value in enumerate(row_data.values()):
            sht.cells(current_row, col + 1).value = value
        current_row += 1

    new_filename = output_filename
    wb.save(new_filename)
    wb.close()
    app.quit()

    return questions
