import gradio as gr
import dashscope
from http import HTTPStatus
import base64
import requests
import time
from pathlib import Path
import os
from dashscope.audio.tts_v2 import *

RESOURCE_PATH = Path(__file__).parent.resolve()


def resolve_resource_path(path):
    """
    解析资源路径：将相对路径与应用的资源路径结合，返回绝对路径。

    参数:
    path (str): 相对资源路径。

    返回:
    Path: 绝对资源路径。
    """
    return Path(RESOURCE_PATH / path).resolve()


def file_to_base64(path):
    with open(path, 'rb') as file:
        encoded_string = base64.b64encode(file.read())
    return encoded_string.decode('utf-8')


def upload_file(file_path):
    """
    上传文件到服务器。

    参数:
    file_path: 文件路径，本地路径或网络URL。

    返回值:
    上传后的文件URL或错误信息。
    """
    file_path = str(resolve_resource_path(file_path))
    if not os.path.exists(file_path):
        return file_path
    upload_url = 'http://47.99.81.126:6500/upload'
    with open(file_path, 'rb') as file:
        files = {'file': file}
        try:
            response = requests.post(upload_url, files=files)
            # 检查请求是否成功
            if response.status_code == 200:
                data = response.json()
                return data['url']
            else:
                raise Exception(
                    'Error Message: {}, Status Code: {}, Response: {}'.format('文件上传失败', response.status_code,
                                                                              response.text))
        except Exception as e:
            raise Exception(f"An error occurred: {e}")


# 大模型文字交互
def text_generation(text, chat_history=[], prompt='你是一个人工智能助手，你的名字叫小H', stream=False):
    """
    与大模型进行文字交互，基于给定的对话历史和提示进行响应生成。

    参数:
    chat_history (list): 对话历史，每个元素为用户或助手的一条消息。
    prompt (str): 提示文本，用于引导模型的响应，默认为"你是一个人工智能助手，你的名字叫小H"。
    stream (bool): 是否以流式方式获取生成结果，默认为False。

    返回:
    str: 模型生成的响应文本，或错误信息。
    """

    try:
        messages = [{'role': 'system', 'content': prompt}]
        messages.extend(chat_history)
        messages.append({'role': 'user', 'content': text})
        response = dashscope.Generation.call(model="qwen-plus",
                                             messages=messages,
                                             result_format='message',
                                             stream=stream)
        if response.status_code == HTTPStatus.OK:
            return response.output.choices[0]['message']['content']
        else:
            return "错误: " + response.message
    except Exception as e:
        return "错误: " + str(e)


# 大模型图像理解
def image_understanding(img, text="", chat_history=[], prompt='你是一名人工智能助手', stream=False):
    """
    大模型对图像进行理解，基于对话历史和图像进行响应生成。

    参数:
    img (str): 图像的本地路径或URL。
    chat_history (list): 对话历史，每个元素为用户或助手的一条消息。
    prompt (str): 提示文本，用于引导模型的响应，默认为"你是一名人工智能助手"。
    stream (bool): 是否以流式方式获取生成结果，默认为False。

    返回:
    str: 模型生成的响应文本，或错误信息。
    """
    try:
        messages = [{'role': 'system', 'content': [{'text': prompt}]}]
        for message in chat_history:
            if not isinstance(message['content'], str):
                url = f"file://{message['content'].file.path}"
                messages.append({'role': message['role'], 'content': [{'image': url}]})
            else:
                messages.append({'role': message['role'], 'content': [{'text': message['content']}]})
        if img:
            messages.append({'role': 'user', 'content': [{'image': f"file://{img}"}, {'text': text}]})
        response = dashscope.MultiModalConversation.call(model='qwen-vl-plus',
                                                         messages=messages,
                                                         stream=stream)
        if response.status_code == HTTPStatus.OK:
            return response.output.choices[0].message.content[0]['text']
        else:
            return "错误: " + response.message
    except Exception as e:
        return "错误: " + str(e)


# 大模型声音理解
def audio_understanding(audio, text="", chat_history=[], prompt='你是一名人工智能助手', stream=False):
    """
    大模型对声音进行理解，基于对话历史和音频进行响应生成。

    参数:
    audio (str): 音频的本地路径或URL。
    chat_history (list): 对话历史，每个元素为用户或助手的一条消息。
    prompt (str): 提示文本，用于引导模型的响应，默认为"你是一名人工智能助手"。
    stream (bool): 是否以流式方式获取生成结果，默认为False。

    返回:
    str: 模型生成的响应文本，或错误信息。
    """

    try:
        messages = [{'role': 'system', 'content': [{'text': prompt}]}]
        for message in chat_history:
            if not isinstance(message['content'], str):
                url = f"file://{message['content'].file.path}"
                messages.append({'role': message['role'], 'content': [{'audio': url}]})
            else:
                if len(messages[-1]['content']) == 1 and 'audio' in messages[-1]['content'][0]:
                    messages[-1]['content'].append({'text': message['content']})
                else:
                    messages.append({'role': message['role'], 'content': [{'text': message['content']}]})
        if audio:
            messages.append({'role': 'user', 'content': [{'audio': f'file://{audio}'}, {'text': text}]})
        response = dashscope.MultiModalConversation.call(model='qwen-audio-turbo',
                                                         messages=messages,
                                                         stream=stream)
        if response.status_code == HTTPStatus.OK:
            return response.output.choices[0].message.content[0]['text']
        else:
            return "错误: " + response.message
    except Exception as e:
        return "错误: " + str(e)


# 大模型图像生成
def image_generation(prompt):
    """
    根据提示文本生成图像。

    参数:
    prompt (str): 提示文本，用于指导图像生成。

    返回:
    str: 生成的图像URL，或错误信息。
    """
    try:
        response = dashscope.ImageSynthesis.async_call(model='wanx-v1',
                                                       prompt=prompt,
                                                       n=1,
                                                       size='1024*1024')
        if response.status_code == HTTPStatus.OK:
            rsp = dashscope.ImageSynthesis.wait(response)
            if rsp.status_code == HTTPStatus.OK:
                return rsp.output.results[0].url
            else:
                return "错误: " + response.message
        else:
            return "错误: " + response.message
    except Exception as e:
        return "错误: " + str(e)


# 大模型人像风格重绘
def human_repaint(img, style=7):
    """
    使用大模型对人像图片进行风格重绘。

    参数:
    img: 图像文件，本地路径或网络URL。
    style: 风格指数，默认为7。

    返回值:
    重绘后的图像URL或错误信息。
    """
    try:
        img_url = upload_file(img)
        url = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': dashscope.api_key,
            'X-DashScope-Async': 'enable',
            'X-DashScope-OssResourceResolve': 'enable'
        }

        params = {
            'model': 'wanx-style-repaint-v1',
            'input': {
                'image_url': img_url,
                'style_index': style
            }
        }

        response = requests.post(url, headers=headers, json=params)
        if response.status_code == 200:
            task_id = response.json()['output']['task_id']
            # 异步任务，轮询任务状态直到完成或失败
            while True:
                time.sleep(3)
                response = requests.get('https://dashscope.aliyuncs.com/api/v1/tasks/{}'.format(task_id),
                                        headers={'Authorization': dashscope.api_key})
                if response.status_code == 200:
                    if response.json()['output']['task_status'] == 'SUCCEEDED':
                        return response.json()['output']['results'][0]['url']
                    elif response.json()['output']['task_status'] == 'FAILED':
                        return "错误: " + response.json()['output']['message']
                else:
                    return "错误: " + response.json()['message']
        else:
            return "错误: " + response.json()['message']
    except Exception as e:
        return "错误: " + str(e)


# 涂鸦作画
def sketch_to_image(img, prompt, style='<anime>'):
    """
    将涂鸦图像转换为现实图像。

    参数:
    img: 涂鸦图像文件，本地路径或网络URL。
    prompt: 描述期望图像的文字提示。
    style: 风格标签，默认为'<anime>'。

    返回值:
    生成的图像URL或错误信息。
    """
    try:
        img_url = upload_file(img)  # 上传图像文件
        url = 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis/'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': dashscope.api_key,
            'X-DashScope-Async': 'enable',
            'X-DashScope-OssResourceResolve': 'enable'
        }

        params = {
            'model': 'wanx-sketch-to-image-lite',
            'input': {
                'sketch_image_url': img_url,
                'prompt': prompt
            },
            'parameters': {
                'size': '768*768',
                'n': 1,
                'style': style
            }
        }

        response = requests.post(url, headers=headers, json=params)
        if response.status_code == 200:
            task_id = response.json()['output']['task_id']
            # 异步任务，轮询任务状态直到完成或失败
            while True:
                time.sleep(3)
                response = requests.get('https://dashscope.aliyuncs.com/api/v1/tasks/{}'.format(task_id),
                                        headers={'Authorization': dashscope.api_key})
                if response.status_code == 200:
                    if response.json()['output']['task_status'] == 'SUCCEEDED':
                        return response.json()['output']['results'][0]['url']
                    elif response.json()['output']['task_status'] == 'FAILED':
                        return "错误: " + response.json()['output']['message']
                else:
                    return "错误: " + response.json()['message']
        else:
            return "错误: " + response.json()['message']
    except Exception as e:
        return "错误: " + str(e)


# 语音识别
def speech_recognition(audio):
    """
    将语音转换为文字。

    参数:
    audio: 语音文件，本地路径或网络URL。

    返回值:
    识别出的文字或错误信息。
    """
    try:
        audio_url = upload_file(audio)  # 上传语音文件
        task_response = dashscope.audio.asr.Transcription.async_call(
            model='paraformer-v2',
            file_urls=[audio_url]
        )
        transcribe_response = dashscope.audio.asr.Transcription.wait(task=task_response.output.task_id)
        if transcribe_response.status_code == HTTPStatus.OK:
            result = transcribe_response.output
            if result['task_status'] == 'SUCCEEDED':
                json_url = result['results'][0]['transcription_url']
                response = requests.get(json_url)
                if response.status_code == 200:
                    data = response.json()
                    return data['transcripts'][0]['text']
                else:
                    return '错误: 结果获取出错'
            else:
                return '错误: 解码错误'
        else:
            return '错误: 解析错误'
    except Exception as e:
        return "错误: " + str(e)


# 语音合成
def speech_synthesis(text, rate=1.0, pitch=1.0, voice='longxiaochun'):
    """
    将文字转换为语音。

    参数:
    text: 要合成的文字。
    rate: 语速调整，默认为1。
    pitch: 语调调整，默认为1。
    voice: 语音音色名，默认为'longxiaochun'。

    返回值:
    合成的语音文件路径或错误信息。
    """
    try:
        synthesizer = SpeechSynthesizer(model='cosyvoice-v1', voice=voice, pitch_rate=pitch, speech_rate=rate)
        result = synthesizer.call(text)
        return base64.b64encode(result).decode('utf-8')
    except Exception as e:
        return "错误: " + str(e)


class AIWebApp:
    def __init__(self, title='My AI Web App'):
        self.title = title
        self.components = []
        self.core_logic = None
        self.api_key = None
        self.mode = None
        self.client = None

        # 用于存储输入数据的属性
        self.input_text = ''
        self.input_pic = None
        self.input_audio = None
        self.chat_history = []

        # 用于存储处理结果的字典
        self.results = {}

    @classmethod
    def set_apikey(cls, key):
        cls.api_key = key
        dashscope.api_key = key
        cls.mode = 'dashscope'

    def add_input_text(self):
        self.components.append({
            'component': gr.Textbox,
            'kwargs': {'label': '文字输入'}
        })

    def add_input_pic(self):
        self.components.append({
            'component': gr.Image,
            'kwargs': {'label': '图像输入', 'type': 'filepath', 'height': 280}
        })

    def add_input_audio(self):
        self.components.append({
            'component': gr.Audio,
            'kwargs': {'label': '音频输入', 'type': 'filepath'}
        })

    def add_submit(self, callback=None):
        """
        添加提交按钮组件，并设置提交时的回调函数。

        :param callback: 学生编写的核心逻辑函数，接受一个参数 self。
        """
        self.core_logic = callback

    def run(self, **kwargs):
        with gr.Blocks(title=self.title) as demo:
            gr.Markdown(f"# {self.title}")
            state = gr.State([])  # 用于存储多轮对话的状态

            with gr.Column():
                with gr.Row():
                    inputs = []
                    for comp_def in self.components:
                        component_class = comp_def['component']
                        component_kwargs = comp_def.get('kwargs', {})
                        component_instance = component_class(**component_kwargs)
                        inputs.append(component_instance)
                with gr.Row():
                    clear_button = gr.ClearButton(components=inputs, value='清除')
                    submit_button = gr.Button('提交', variant='primary')

                # 显示对话历史的组件
                chat_history = gr.Chatbot(type='messages', label='对话记录')

            def gradio_callback(*args):
                # 提取输入参数和状态
                *user_inputs, chat_history_state = args

                self.chat_history = chat_history_state
                # 重置输入属性
                self.input_text = ''
                self.input_pic = None
                self.input_audio = None

                # 根据添加的组件，按顺序获取输入数据并存储到属性中
                idx = 0
                for comp_def in self.components:
                    component_class = comp_def['component']
                    comp_name = component_class.__name__
                    if comp_name == 'Textbox':
                        self.input_text = user_inputs[idx]
                        idx += 1
                    elif comp_name == 'Image':
                        self.input_pic = user_inputs[idx]
                        idx += 1
                    elif comp_name == 'Audio':
                        self.input_audio = user_inputs[idx]
                        idx += 1

                # 初始化对话历史
                if not chat_history_state:
                    chat_history_state = []

                # 构建用户的多模态输入消息
                if self.input_pic:
                    chat_history_state.append({"role": "user", "content": {"path": self.input_pic, "alt_text": "用户输入图像"}})
                if self.input_audio:
                    chat_history_state.append({"role": "user", "content": {"path": self.input_audio, "alt_text": "用户输入音频"}})
                if self.input_text:
                    chat_history_state.append({"role": "user", "content": self.input_text})

                # 重置结果字典
                self.results = {}

                # 调用学生编写的核心逻辑函数
                self.core_logic()

                # 构建 AI 的回复消息
                if 'image' in self.results:
                    chat_history_state.append({"role": "assistant", "content": f'![AI图像]({self.results["image"]})'})
                if 'audio' in self.results:
                    audio_b64 = self.results['audio']
                    chat_history_state.append({"role": "assistant", "content": f'<audio controls autoplay><source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3"></audio>'})
                if 'text' in self.results:
                    chat_history_state.append({"role": "assistant", "content": self.results['text']})

                # 构建用于重置输入组件的值
                reset_values = []
                for comp_def in self.components:
                    component_class = comp_def['component']
                    comp_name = component_class.__name__
                    if comp_name == 'Textbox':
                        reset_values.append('')  # 重置文本框为空字符串
                    elif comp_name == 'Image':
                        reset_values.append(None)  # 重置图像组件为 None
                    elif comp_name == 'Audio':
                        reset_values.append(None)  # 重置音频组件为 None
                    else:
                        reset_values.append(None)

                return [chat_history_state, chat_history_state] + reset_values

            submit_button.click(
                fn=gradio_callback,
                inputs=inputs + [state],
                outputs=[chat_history, state] + inputs,
                queue=True
            )

        demo.launch(**kwargs)