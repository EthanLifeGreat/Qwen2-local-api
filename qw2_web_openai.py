# Copyright (c) Alibaba Cloud.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

"""A simple web interactive chat demo based on gradio."""

from argparse import ArgumentParser
import gradio as gr
from openai import OpenAI

max_tokens = 8192
# do_sample = True
top_p = 0.9
temperature = 1.0
# top_k = 1
# repetition_penalty = 1.0

# Set OpenAI's API key and API base to use vLLM's API server.
openai_api_key = "EMPTY"
openai_api_base = "http://0.0.0.0:8008/v1"
client = OpenAI(
    api_key=openai_api_key,
    base_url=openai_api_base,
)


def _get_args():
    parser = ArgumentParser()
    parser.add_argument("--share", action="store_true", default=False,
                        help="Create a publicly shareable link for the interface.")
    parser.add_argument("--inbrowser", action="store_true", default=False,
                        help="Automatically launch the interface in a new tab on the default browser.")
    parser.add_argument("--server-port", type=int, default=8000,
                        help="Demo server port.")
    parser.add_argument("--server-name", type=str, default="0.0.0.0",
                        help="Demo server name.")

    args = parser.parse_args()
    return args


def _gc():
    import gc
    gc.collect()


def _launch_demo(args):

    def predict(_query, _chatbot, _task_history):
        print(f"User: {_query}")
        _chatbot.append((_query, ""))

        conversation = [
            {'role': 'system', 'content': "你是一个能够提供帮助和建议的人工智能助手。"},
        ]
        for query_h, response_h in _task_history:
            conversation.append({'role': 'user', 'content': query_h})
            conversation.append({'role': 'assistant', 'content': response_h})
        conversation.append({'role': 'user', 'content': _query})

        full_response = ""
        response = ""
        # Get Streaming response from API
        response_stream = client.chat.completions.create(
            model="Qwen2-72B-Instruct-GPTQ-Int4",
            messages=conversation,
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=top_p,
            stream=True
        )
        for chunk in response_stream:
            chunk_message = chunk.choices[0].delta.content
            if not chunk_message or chunk_message == '':  # if the message is empty, skip it
                continue
            response += chunk_message
            _chatbot[-1] = (_query, response)
            yield _chatbot
            full_response = response

        print(f"History: {_task_history}")
        _task_history.append((_query, full_response))
        print(f"Qwen2-Instruct: {full_response}")

    def regenerate(_chatbot, _task_history):
        if not _task_history:
            yield _chatbot
            return
        item = _task_history.pop(-1)
        _chatbot.pop(-1)
        yield from predict(item[0], _chatbot, _task_history)

    def reset_user_input():
        return gr.update(value="")

    def reset_state(_chatbot, _task_history):
        _task_history.clear()
        _chatbot.clear()
        _gc()
        return _chatbot

    js_func = """
    function refresh() {
        const url = new URL(window.location);
        if (url.searchParams.get('__theme') !== 'dark') {
            url.searchParams.set('__theme', 'dark');
            window.location.href = url.href;
        }
    }
    """

    with gr.Blocks(title='Qwen2-72B Chatbot', js=js_func) as demo:
        gr.Markdown(
            """<p align="center"><img src="https://www.siat.ac.cn/images/logo2016.png?v1.0" 
            style="height: 60px"/><p>""")
        gr.Markdown("""<center><font size=8>Qwen2-72B Chatbot</center>""")
        gr.Markdown(
            """\
<center><font size=3>本聊天机器人由中国科学院深圳先进技术研究院环绕智能与多模态系统研究室基于Qwen2-72B-Chat打造，实现聊天机器人功能。</center>""")
        gr.Markdown("""\
<center><font size=4>
Qwen2-7B-Instruct <a href="https://modelscope.cn/models/qwen/Qwen2-7B-Instruct/summary">🤖 </a> | 
<a href="https://huggingface.co/Qwen/Qwen2-7B-Instruct">🤗</a>&nbsp ｜ 
Qwen2-72B-Instruct <a href="https://modelscope.cn/models/qwen/Qwen2-72B-Instruct/summary">🤖 </a> | 
<a href="https://huggingface.co/Qwen/Qwen2-72B-Instruct">🤗</a>&nbsp ｜ 
&nbsp<a href="https://github.com/QwenLM/Qwen2">Github</a></center>""")

        chatbot = gr.Chatbot(label='Qwen2-72B', elem_classes="control-height", show_copy_button=True)
        query = gr.Textbox(lines=2, label='Input')
        task_history = gr.State([])

        with gr.Row():
            empty_btn = gr.Button("🧹 Clear History (清除历史)")
            submit_btn = gr.Button("🚀 Submit (发送)")
            regen_btn = gr.Button("🤔️ Regenerate (重试)")

        submit_btn.click(predict, [query, chatbot, task_history], [chatbot], show_progress="full")
        submit_btn.click(reset_user_input, [], [query])
        empty_btn.click(reset_state, [chatbot, task_history], outputs=[chatbot], show_progress="full")
        regen_btn.click(regenerate, [chatbot, task_history], [chatbot], show_progress="full")

    demo.queue().launch(
        share=args.share,
        inbrowser=args.inbrowser,
        server_port=args.server_port,
        server_name=args.server_name,
    )


def main():
    args = _get_args()

    _launch_demo(args)


if __name__ == '__main__':
    main()
