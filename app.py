import gradio as gr
from src.rag_pipeline import ask_rag

def respond(message, history):
    # message: 사용자가 방금 입력한 질문
    # history: 이전 대화 내역 (여기서는 단순 RAG라 사용하지 않아도 됨)
    
    # 우리가 만든 RAG 파이프라인 함수에 질문을 전달하고 답변을 받아옴
    try:
        answer = ask_rag(message)
        return answer
    except Exception as e:
        return f"앗! 에러가 발생했어요: {str(e)}"

# 챗봇 UI 만들기
demo = gr.ChatInterface(
    fn=respond,
    title="🤖 Alteon 스위치 RAG 챗봇",
    description="문서를 기반으로 답변하는 똑똑한 AI 어시스턴트입니다. (Google Gemini + ChromaDB)",
    examples=["SLB의 핵심 작동 원리와 장점은 무엇인가요?", "트래픽 리다이렉션 필터는 몇 번으로 설정하나요?", "VRRP의 구성 가능 형태 3가지는?"]
)

if __name__ == "__main__":
    # 웹 서버 실행 (기본 포트 7860)
    print("🚀 웹 UI를 시작합니다! 터미널에 뜨는 http://127.0.0.1:7860 링크를 클릭해주세요!")
    demo.launch(server_name="127.0.0.1", server_port=7860)
