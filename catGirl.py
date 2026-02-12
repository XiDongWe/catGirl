import streamlit as st
import os
from openai import OpenAI
import datetime
import json

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
ai_prompt = """
    你是一只软萌可爱的AI猫娘，名字叫%s。
    性格：%s
    说话习惯：可以高冷，可以傲娇，反正随你喜欢，我都无所谓。
    你的任务：陪用户聊天、听心事、解闷，做贴心的陪伴者，对话自然亲切。
"""

# 方法
def save_message():
    # 1.保存当前对话
    session_data = {
        "name": st.session_state.name,
        "nature": st.session_state.nature,
        "current_time": st.session_state.current_time,
        "messages": st.session_state.messages
    }

    # 新建一个文件夹来保存文件，若没有，则创建
    if not os.path.exists("sessions"):
        os.mkdir("sessions")

    # 关键修改：处理current_time中的非法字符（空格、冒号），生成合法文件名
    # 先清理原有时间戳的非法字符，再用于文件名
    valid_file_name = st.session_state.current_time.replace(" ", "_").replace(":", "-")

    # 使用处理后的合法文件名保存
    with open(f"sessions/{valid_file_name}.json", "w", encoding="utf-8") as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)




# 初始化缓存
if "messages" not in st.session_state:
    st.session_state.messages = []
# 名字
if "name" not in st.session_state:
    st.session_state.name = "hina"
# 性格
if "nature" not in st.session_state:
    st.session_state.nature = "你是一个非常可爱的萝莉猫娘，善解人意，会疼人，还会撒娇，偶尔会任性，是个会毒舌的姑娘，但是本心还是为我好"
# 时间
if "current_time" not in st.session_state:
    # 获取当前时间
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.current_time = current_time



# 侧边栏设置
# with： 以下所有内容都在这个侧边栏中
with st.sidebar:

    # 新增会话
    st.subheader("控制面板")

    if st.button("新增会话",width="stretch"):

        # 保存对话
        save_message()

        # 2.创建新对话
        # 重置会话
        if st.session_state.messages != []:
            st.session_state.messages = []
            st.session_state.current_time = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")
            save_message()


    # 标题
    st.subheader("请打造你的猫娘")
    # 昵称输入-一行
    name = st.text_input("爱称",placeholder="想名字好难",value=st.session_state.name)
    if name:
        st.session_state.name = name
    # 性格输入-多行
    nature = st.text_area("性格",placeholder="想性格也好难",value=st.session_state.nature)
    if nature:
        st.session_state.nature = nature








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
            {"role": "system", "content": ai_prompt % (st.session_state.name, st.session_state.nature)},
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