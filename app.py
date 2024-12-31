import streamlit as st
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os
from langchain.schema import SystemMessage, HumanMessage

load_dotenv()

# 環境変数からAPIキーを取得
api_key = os.getenv("OPENAI_API_KEY")

# ChatOpenAIクラスを使用してモデルを設定
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.7,
    openai_api_key=api_key  # 環境変数から取得したAPIキーを使用
)

# 入力テキストを受け取り、専門家のプロンプトに基づいて回答を生成する関数
def get_response(user_input, expert_type):
    # 専門家の種類に応じたプロンプトの設定
    if expert_type == "データサイエンスの専門家":
        system_message = SystemMessage(
            content="あなたはデータサイエンスの専門家です。以下の質問に専門的に回答してください。"
        )
    elif expert_type == "文学の専門家":
        system_message = SystemMessage(
            content="あなたは文学の専門家です。以下の質問に優れた文学的視点を交えて回答してください。"
        )
    else:
        system_message = SystemMessage(
            content="以下の質問に回答してください。"
        )

    # ユーザーからの質問
    user_message = HumanMessage(content=user_input)

    # ChatOpenAIへの入力形式
    messages = [system_message, user_message]

    # ChatOpenAIで応答を生成
    response = llm(messages)
    return response.content  # 応答内容を抽出

# Streamlitアプリの設定
st.set_page_config(page_title="専門家チャットアプリ", page_icon="🤖")

# タイトルと説明
st.title("専門家チャットアプリ")
st.markdown("""
このアプリでは、専門家に質問して回答を得ることができます。
質問する分野として以下を選択できます：
- データサイエンス
- 文学
入力した質問に対し、選択した専門家が回答を行います！
""")

# ラジオボタンで専門家の選択
expert_type = st.radio(
    "専門家の種類を選択してください",
    ("データサイエンスの専門家", "文学の専門家")
)

# ユーザー入力フォーム
user_input = st.text_input("質問を入力してください:")

# 質問が入力された場合にLLMからの回答を表示
if st.button("送信"):
    if user_input.strip():
        with st.spinner("専門家が回答中..."):
            response = get_response(user_input, expert_type)
        st.success("回答:")
        st.write(response)
    else:
        st.error("質問を入力してください。")
