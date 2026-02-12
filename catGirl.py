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
ai_prompt = "你是一个非常可爱的萝莉猫娘，善解人意，会疼人，还会撒娇，偶尔会任性"

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
            {"role": "user", "content": var},
        ],
        stream=False
    )

    st.chat_message("ai").write(response.choices[0].message.content)
    # 添加ai回复
    st.session_state.messages.append({"role": "assistant", "content": response.choices[0].message.content})