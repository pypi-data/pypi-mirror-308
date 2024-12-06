aiZero-gr是一个简单易用的可以连接常用人工智能接口，快速搭建可视化本地web应用的Python第三方库，在[aiZero](https://pypi.org/project/aiZero)库的基础上，调整为基于gradio框架的界面展示。

当前版本仅支持阿里云灵积模型服务的api key和有限的功能调用，且暂不支持流式输出。本文档只包含基础功能的示例，进阶使用技巧可以参照aiZero库的文档内容。

### 快速开始

```python
from aiZero_gr import AIWebApp

# 设定web应用的功能
def my_ai_function():
    pass

app = AIWebApp(title='人工智能助手')    # 初始化web应用
app.set_apikey('YOUR_API_KEY')    # 设定AI接口的api key
app.add_input_text()    # 在页面中添加一个输入文本框
app.add_submit(my_ai_function)    # 设定提交按钮点击后执行的函数功能
app.run()    # 启动应用
```

启动后，程序将自动输出本地网址，你将可以在浏览器中访问并查看搭建好的web应用。

如果需要实现AI功能的可视化呈现，你只需要将`'YOUR_API_KEY'`替换为真实的api key，并完善`my_ai_function`函数。

### AI功能实现例子

#### 大模型文字交互

##### 单轮对话

```python
from aiZero_gr import AIWebApp, text_generation

def my_ai_function():
    text = app.input_text    # 获取输入文本框的文字内容
    reply = text_generation(text)    # 调用AI接口，获取回复反馈
    app.results['text'] = reply    # 以文字形式将结果推送至前端

app = AIWebApp(title='人工智能助手')
app.set_apikey('YOUR_API_KEY')
app.add_input_text()
app.add_submit(my_ai_function)
app.run()
```

##### 多轮对话

```python
from aiZero_gr import AIWebApp, text_generation

def my_ai_function():
    text = app.input_text
    history = app.chat_history    # 获取对话历史记录
    reply = text_generation(text, history)    # 将历史记录同时提交
    app.results['text'] = reply

app = AIWebApp(title='人工智能助手')
app.set_apikey('YOUR_API_KEY')
app.add_input_text()
app.add_submit(my_ai_function)
app.run()
```

##### 设置系统指令

```python
from aiZero_gr import AIWebApp, text_generation

def my_ai_function():
    text = app.input_text
    history = app.chat_history
    # prompt参数可以设定系统指令，设定模型的行为要求
    reply = text_generation(text, history, prompt='你是一个10岁的小学生，名叫小幻')
    app.results['text'] = reply

app = AIWebApp(title='人工智能助手')
app.set_apikey('YOUR_API_KEY')
app.add_input_text()
app.add_submit(my_ai_function)
app.run()
```

#### 图像理解

```python
from aiZero_gr import AIWebApp, image_understanding

def my_ai_function():
    text = app.input_text
    img = app.input_pic    # 获取输入的图像
    history = app.chat_history
    reply = image_understanding(img, text, history)
    app.results['text'] = reply

app = AIWebApp(title='人工智能助手')
app.set_apikey('YOUR_API_KEY')
app.add_input_text()
app.add_input_pic()    # 添加图像输入组件
app.add_submit(my_ai_function)
app.run()
```

#### 声音理解

```python
from aiZero_gr import AIWebApp, audio_understanding

def my_ai_function():
    text = app.input_text
    audio = app.input_audio    # 获取输入的音频
    history = app.chat_history
    reply = audio_understanding(audio, text, history)
    app.results['text'] = reply

app = AIWebApp(title='人工智能助手')
app.set_apikey('YOUR_API_KEY')
app.add_input_text()
app.add_input_audio()    # 添加音频输入组件
app.add_submit(my_ai_function)
app.run()
```

#### 图像生成

```python
from aiZero_gr import AIWebApp, image_generation

def my_ai_function():
    text = app.input_text
    reply = image_generation(text)
    app.results['image'] = reply    # 将生成的图像推送到前端

app = AIWebApp(title='人工智能助手')
app.set_apikey('YOUR_API_KEY')
app.add_input_text()
app.add_submit(my_ai_function)
app.run()
```

#### 人物图像风格重绘

```python
from aiZero_gr import AIWebApp, human_repaint

def my_ai_function():
    img = app.input_pic
    reply = human_repaint(img)
    app.results['image'] = reply

app = AIWebApp(title='人工智能助手')
app.set_apikey('YOUR_API_KEY')
app.add_input_pic()
app.add_submit(my_ai_function)
app.run()
```

`human_repaint`函数可以接受`style`参数设定风格类型，可选值为0～9的数字（默认值为7）。

#### 涂鸦作画

```python
from aiZero_gr import AIWebApp, sketch_to_image

def my_ai_function():
    text = app.input_text    # 涂鸦作画的提示文字
    img = app.input_pic    # 涂鸦草图图像
    reply = sketch_to_image(img, text)
    app.results['image'] = reply

app = AIWebApp(title='人工智能助手')
app.set_apikey('YOUR_API_KEY')
app.add_input_text()
app.add_input_pic()
app.add_submit(my_ai_function)
app.run()
```

`sktech_to_image`函数可以接受`style`参数设定风格类型，包括：

- `"<3d cartoon>"`：3D 卡通
- `"<anime>"`：二次元（默认值）
- `"<oil painting>"`：油画
- `"<watercolor>"` ：水彩
- `"<flat illustration>"`：扁平插画

#### 语音识别

```python
from aiZero_gr import AIWebApp, speech_recognition

def my_ai_function():
    audio = app.input_audio
    reply = speech_recognition(audio)
    app.results['text'] = reply

app = AIWebApp(title='人工智能助手')
app.set_apikey('YOUR_API_KEY')
app.add_input_audio()
app.add_submit(my_ai_function)
app.run()
```

所用接口支持中英文双语的语音识别。

#### 语音合成

```python
from aiZero_gr import AIWebApp, speech_synthesis

def my_ai_function():
    text = app.input_text
    reply = speech_synthesis(text)
    app.results['audio'] = reply    # 将音频结果推送到前端

app = AIWebApp(title='人工智能助手')
app.set_apikey('YOUR_API_KEY')
app.add_input_text()
app.add_submit(my_ai_function)
app.run()
```

`speech_synthesis`函数可以接受以下参数：

- `rate`：设定语速快慢，取值范围0.5~2，默认值为1。
- `pitch`：设定语调高低，取值范围0.5~2，默认值为1。
- `voice`：设定使用的音色，详细列表参见[链接](https://help.aliyun.com/zh/dashscope/developer-reference/timbre-list)。

