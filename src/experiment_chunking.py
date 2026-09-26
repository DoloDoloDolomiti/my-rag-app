import os
import time
import chromadb
from google import genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=api_key)

db_path = os.path.join(os.path.dirname(__file__), '..', 'chroma_db')
chroma_client = chromadb.PersistentClient(path=db_path)

file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'alteon_guide.txt')
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

chunk_sizes = [100, 200, 300, 400]
test_query = "SLB의 로드 밸런싱 정책 중 Persistence-based 알고리즘에는 어떤 것들이 있으며 각각 어떤 특징이 있나요?"

print(f"🔍 실험 질문: {test_query}\n")

results = []

for size in chunk_sizes:
    print(f"==== 청크 크기: {size} ====")
    # 1. 청킹
    chunks = [text[i:i+size] for i in range(0, len(text), size)]
    print(f"생성된 청크 수: {len(chunks)}개")
    
    # 2. 컬렉션 생성
    collection_name = f"alteon_exp_{size}"
    try:
        chroma_client.delete_collection(name=collection_name)
    except:
        pass
    collection = chroma_client.create_collection(name=collection_name)
    
    # 3. 임베딩 및 저장 (시간 측정)
    start_time = time.time()
    for i, chunk in enumerate(chunks):
        response = client.models.embed_content(
            model='gemini-embedding-2',
            contents=chunk,
        )
        embedding = response.embeddings[0].values
        collection.add(
            ids=[f"chunk_{i}"],
            embeddings=[embedding],
            documents=[chunk],
            metadatas=[{"chunk_index": i}]
        )
    embed_time = time.time() - start_time
    
    # 4. 검색
    query_response = client.models.embed_content(
        model='gemini-embedding-2',
        contents=test_query,
    )
    query_embedding = query_response.embeddings[0].values
    
    # 상위 3개 검색
    search_results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )
    
    retrieved_docs = search_results['documents'][0]
    context = "\n\n---\n\n".join(retrieved_docs)
    
    # 5. 답변 생성
    prompt = f"""당신은 제공된 참고 문서만을 기반으로 친절하게 답변하는 AI 어시스턴트입니다.
만약 참고 문서에 질문에 대한 답이 없다면, "문서에 해당 내용이 없습니다"라고 말해주세요.

[참고 문서]
{context}

[질문]
{test_query}
"""
    answer = client.models.generate_content(
        model='gemini-flash-latest',
        contents=prompt
    )
    
    print(f"찾아낸 문서 길이: {len(context)}자")
    print(f"답변: {answer.text.strip()}\n")
    
    results.append({
        "size": size,
        "chunk_count": len(chunks),
        "embed_time": f"{embed_time:.2f}초",
        "retrieved_context": context,
        "answer": answer.text.strip()
    })

# 결과를 Markdown 파일로 저장하기 위해 포맷팅
md_content = "# 청크 크기(Chunk Size)별 RAG 성능 비교 실험 결과\n\n"
md_content += f"**실험 질문:** `{test_query}`\n\n"
md_content += "> 동일한 질문에 대해 문서 조각 크기(100, 200, 300, 400자)를 다르게 했을 때, 검색되는 내용과 AI의 답변 품질이 어떻게 달라지는지 비교합니다.\n\n---\n\n"

for res in results:
    md_content += f"## 📏 청크 크기: {res['size']}자\n"
    md_content += f"- **생성된 총 청크 수:** {res['chunk_count']}개\n"
    md_content += f"- **임베딩 소요 시간:** {res['embed_time']}\n"
    md_content += f"### 🔍 검색된 문맥 (상위 3개 청크, 총 {len(res['retrieved_context'])}자)\n"
    md_content += f"```text\n{res['retrieved_context']}\n```\n"
    md_content += f"### 🤖 Gemini의 답변\n> {res['answer']}\n\n"
    md_content += "---\n\n"

with open("/Users/aaa/.gemini/antigravity-ide/brain/d110af6a-65b7-4aca-8a37-a8e5790f313e/experiment_results.md", "w", encoding="utf-8") as f:
    f.write(md_content)

print("✅ 실험 완료! 결과가 experiment_results.md 에 저장되었습니다.")
