import os
import chromadb
from google import genai
from dotenv import load_dotenv

# 1. 환경 설정 및 API 연결
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    try:
        import streamlit as st
        api_key = st.secrets.get("GOOGLE_API_KEY")
    except Exception:
        pass
client = genai.Client(api_key=api_key)

# 2. 벡터 DB 연결 (저장된 문서 가져오기)
db_path = os.path.join(os.path.dirname(__file__), '..', 'chroma_db')
chroma_client = chromadb.PersistentClient(path=db_path)

def get_collection():
    try:
        return chroma_client.get_collection(name="alteon_collection")
    except Exception:
        # DB가 없을 경우 자동으로 alteon_guide.txt 문서를 읽어 DB 구축
        file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'alteon_guide.txt')
        collection = chroma_client.get_or_create_collection(name="alteon_collection")
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
            chunk_size = 400
            chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
            for i, chunk in enumerate(chunks):
                response = client.models.embed_content(
                    model='gemini-embedding-2',
                    contents=chunk,
                )
                embedding = response.embeddings[0].values
                collection.upsert(
                    ids=[f"chunk_{i}"],
                    embeddings=[embedding],
                    documents=[chunk],
                    metadatas=[{"source": "alteon_guide.txt", "chunk_index": i}]
                )
        return collection

def ask_rag(query: str) -> str:
    collection = get_collection()
    # 3. 사용자 질문을 임베딩(벡터화)
    response = client.models.embed_content(
        model='gemini-embedding-2',
        contents=query,
    )
    query_embedding = response.embeddings[0].values
    
    # 4. DB에서 가장 유사한 조각 2개 찾기 (Retrieval)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=2
    )
    
    # 검색된 텍스트들을 하나로 합침
    retrieved_docs = results['documents'][0]
    context = "\n\n---\n\n".join(retrieved_docs)
    
    # 5. 프롬프트 만들기 (검색된 내용 + 질문)
    prompt = f"""당신은 제공된 참고 문서만을 기반으로 친절하게 답변하는 AI 어시스턴트입니다.
만약 참고 문서에 질문에 대한 답이 없다면, "문서에 해당 내용이 없습니다"라고 말해주세요.

[참고 문서]
{context}

[질문]
{query}
"""

    # 6. Gemini에게 프롬프트 전송 및 답변 받기
    answer = client.models.generate_content(
        model='gemini-flash-latest',
        contents=prompt
    )
    
    return answer.text

if __name__ == "__main__":
    # 질문 예시 1: SLB란?
    print(ask_rag("SLB의 핵심 작동 원리와 장점은 무엇인가요?"))
    
    # 질문 예시 2: 필터 설정
    print(ask_rag("트래픽 리다이렉션 필터는 몇 번으로 설정하나요?"))
