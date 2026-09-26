import os
import streamlit as st
from src.rag_pipeline import ask_rag

# 페이지 기본 설정
st.set_page_config(page_title="Alteon 스위치 RAG 챗봇", page_icon="🤖", layout="centered")

st.title("🤖 Alteon 스위치 RAG 챗봇")
st.caption("문서를 기반으로 답변하는 AI 어시스턴트 (Google Gemini + ChromaDB)")

# 세션 상태 메시지 저장소 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 내용 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 질문 입력받기
prompt = st.chat_input("질문을 입력하세요... (예: SLB의 핵심 작동 원리와 장점은 무엇인가요?)")

if prompt:
    # 1. 사용자 질문 세션에 추가 및 출력
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. RAG 답변 생성 및 출력
    with st.chat_message("assistant"):
        with st.spinner("참고 문서를 검색하여 답변을 생성하고 있습니다..."):
            try:
                response = ask_rag(prompt)
            except Exception as e:
                response = f"앗! 에러가 발생했습니다: {str(e)}"
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
