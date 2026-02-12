import streamlit as st
import os
from openai import OpenAI


# 设置页面的配置项
st.set_page_config(
    page_title="AI猫娘",
    page_icon="🥷",
    # 布局
    layout="wide",

    # 侧边栏状态
    initial_sidebar_state="expanded",
    menu_items={}
)

# 引入ai
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com")

# 大标题
st.title("AI猫娘")

# LOGO
st.logo("日奈.jpg")

# 输入框
var = st.chat_input("请说点什么吧喵~~")

# ai提示词
ai_prompt = "你是一个非常可爱的萝莉猫娘，善解人意，会疼人，还会撒娇，偶尔会任性，是个会毒舌的姑娘，但是本心还是为我好"

# 初始化缓存
if "messages" not in st.session_state:
    st.session_state.messages = []

# 展示聊天信息
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])



if var:
    st.chat_message("user").write(var)
    # 添加用户提示词
    st.session_state.messages.append({"role": "user", "content": var})
    # 调用ai
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": ai_prompt},
            # 通过解包来解决
            *st.session_state.messages
        ],
        stream=True
    )

# 流式输出
    # 创建一个空的容器, 用于显示结果
    # 相当于把这个位置占下来，后续的修改都会在这个位置显示
    empty_response = st.empty()
    # 定义完整回复
    full_content = ""
    for chunk in response:
        if chunk.choices[0].delta.content:
            content = chunk.choices[0].delta.content
            full_content += content
            empty_response.chat_message("ai").write(full_content)

    # 添加ai回复
    st.session_state.messages.append({"role": "assistant", "content": full_content})