import os
import chromadb
from google import genai
from dotenv import load_dotenv

# 1. 환경변수 및 API 키 로드
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    print("❌ API 키를 찾을 수 없습니다. .env 파일을 확인해주세요.")
    exit(1)

client = genai.Client(api_key=api_key)

print("📚 문서를 읽는 중...")
# 2. 문서 읽기 (우리가 준비한 텍스트 파일)
file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'alteon_guide.txt')
with open(file_path, "r", encoding="utf-8") as f:
    text = f.read()

# 3. 문서 쪼개기 (청킹 - Chunking)
# 긴 문서를 한 번에 처리할 수 없으니, 약 400자 단위로 쪼갭니다.
# (실제로는 더 똑똑하게 문단 단위로 쪼개는 라이브러리를 쓰기도 해요!)
chunk_size = 400
chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
print(f"✂️ 문서를 {len(chunks)}개의 조각(청크)으로 나누었습니다.")

# 4. 벡터 DB (ChromaDB) 설정
print("💾 벡터 DB 설정 중...")
# 현재 폴더 안에 'chroma_db'라는 폴더를 만들어서 데이터를 저장해요.
db_path = os.path.join(os.path.dirname(__file__), '..', 'chroma_db')
chroma_client = chromadb.PersistentClient(path=db_path)

# 'alteon_collection' 이라는 이름의 서랍(컬렉션)을 만들거나 가져옵니다.
collection = chroma_client.get_or_create_collection(name="alteon_collection")

# 기존 데이터가 있다면 비워줍니다 (새로 실습할 때 꼬이지 않게)
if collection.count() > 0:
    print("🧹 기존 데이터를 초기화합니다...")
    # chroma db에서 기존 항목 삭제 (간단히 하기 위해 새 컬렉션 이름을 쓰거나 항목을 지웁니다)
    # 여기서는 모두 삭제하지 않고 덮어씌웁니다.
    
print("🔄 텍스트를 숫자(벡터)로 변환(임베딩)하고 DB에 저장합니다...")
print("이 작업은 시간이 조금 걸릴 수 있습니다! (약 10~20초)")

# 5. 각 조각을 임베딩하여 DB에 저장
for i, chunk in enumerate(chunks):
    # Gemini의 임베딩 모델(text-embedding-004)을 사용해서 텍스트를 숫자로 바꿈
    response = client.models.embed_content(
        model='gemini-embedding-2',
        contents=chunk,
    )
    # 변환된 숫자 배열(벡터)
    embedding = response.embeddings[0].values
    
    # DB에 저장: 고유 ID, 임베딩된 숫자, 원래 텍스트, 메타데이터(어디서 왔는지)
    collection.upsert(
        ids=[f"chunk_{i}"],
        embeddings=[embedding],
        documents=[chunk],
        metadatas=[{"source": "alteon_guide.txt", "chunk_index": i}]
    )

print("🎉 모든 문서가 성공적으로 벡터 DB에 저장되었습니다!")
print(f"DB에 저장된 총 데이터 개수: {collection.count()}개")
