import gradio as gr
from question_generator import generate_and_write_to_excel1
from question_generator import generate_and_write_to_excel2

# def gradio_interface():
#     inputs = [
#         gr.Textbox(label="Subject"),
#         gr.Dropdown(label="Question Type", choices=["单选题", "多选题"]),
#         gr.Slider(label="Difficulty (1-5)", minimum=1, maximum=5, step=1),
#         gr.Slider(label="Number of Questions", minimum=1, maximum=10, step=1),
#         gr.Slider(label="Score", minimum=0, maximum=5, step=0.1),
#         gr.Textbox(label="Knowledge (Optional)"),
#         gr.Textbox(label="Tags (Optional)"),
#         gr.File(label="Excel Template", type="xlsx", accept=".xlsx", default="小雅导入题目模板v2.1.2200.xlsx"),
#     ]
#
#     outputs = [
#         gr.Markdown(label="Generated Questions"),
#         gr.File(label="Output Excel File", type="filepath"),
#     ]
#
#     def generate_and_display(*args, **kwargs):
#         subject, question_type, difficulty, num_questions, score, knowledge, tags, excel_template = args
#         output_filename = "小雅导入题目结果_v2.1.2200_with_data.xlsx"
#
#         questions = generate_and_write_to_excel(subject, question_type, difficulty, num_questions, score, knowledge,
#                                                 tags, excel_template, output_filename)
#         markdown_output = "\n".join(
#             [f"- **{q['题干']}**\n   正确答案: {q['正确答案']}\n   答案解析: {q['答案解析']}" for q in questions])
#
#         return markdown_output, output_filename
#
#     iface = gr.Interface(
#         fn=generate_and_display,
#         inputs=inputs,
#         outputs=outputs,
#         title="题目生成器",
#         description="使用Gradio创建的题目生成器，可生成指定类型的题目并将其写入Excel模板。",
#     )
#
#     return iface
#
#
# iface = gradio_interface()
# iface.launch()
inputs = [
    gr.Dropdown(label="模型选择", choices=["gemini", "spark"]),
    gr.Textbox(label="学科"),
    gr.Dropdown(label="题目类型", choices=["单选题", "多选题", "判断题", "填空题"]),
    gr.Slider(label="难度系数 (1-5)", minimum=1, maximum=5, step=1),
    gr.Slider(label="题目数量", minimum=1, maximum=10, step=1),
    gr.Slider(label="分值", minimum=0, maximum=5, step=0.5),
    gr.Textbox(label="知识点 (可选)"),
    gr.Textbox(label="标签 (可选)"),
    # gr.File(label="小雅模板", type="filepath"),
]
outputs = [
    gr.Markdown(label="Generated Questions"),
    gr.File(label="Output Excel File", type="filepath"),
]


def generate_and_display(*args, **kwargs):
    # subject, question_type, difficulty, num_questions, score, knowledge, tags, excel_template = args
    model, subject, question_type, difficulty, num_questions, score, knowledge, tags = args
    output_filename = "小雅导入题目结果_v2.1.2200_with_data.xlsx"
    if model == "gemini":
        questions = generate_and_write_to_excel1(subject, question_type, difficulty, num_questions, score, knowledge,
                                                tags, output_filename)
    else:
        if model == "spark":
            questions = generate_and_write_to_excel2(subject, question_type, difficulty, num_questions, score, knowledge,
                                                    tags, output_filename)
    markdown_output = "\n".join(
        [f"- **{q['题干']}**\n   正确答案: {q['正确答案']}\n   答案解析: {q['答案解析']}" for q in questions])
    return markdown_output, output_filename


iface = gr.Interface(
    fn=generate_and_display,
    inputs=inputs,
    outputs=outputs,
    title="题目生成器",
    description="使用Gradio创建的题目生成器，可生成指定类型的题目并将其写入Excel模板。",
)
iface.launch(share=True)