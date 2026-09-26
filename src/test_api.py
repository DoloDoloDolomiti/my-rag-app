import os
from dotenv import load_dotenv
from google import genai

# 1. .env 파일에서 환경변수 로드
load_dotenv()

# 2. API 키 가져오기
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ 에러: .env 파일에 GOOGLE_API_KEY가 없습니다!")
    print("Google AI Studio에서 API 키를 발급받아 .env 파일에 추가해주세요.")
    exit(1)

print("✅ API 키 로드 완료!")

# 3. Gemini 클라이언트 생성
try:
    client = genai.Client(api_key=api_key)
    
    # 4. 간단한 테스트 질문 보내기
    print("\n🤖 Gemini에게 인사하는 중...")
    response = client.models.generate_content(
        model='gemini-flash-latest',
        contents='안녕, 넌 누구니? 한 줄로 대답해줘.'
    )
    
    print("\n✨ Gemini의 답변:")
    print(response.text)
    
except Exception as e:
    print(f"\n❌ API 호출 중 에러 발생: {e}")
