FROM python:3.11-slim

WORKDIR /app

# 시스템 필수 패키지 설치 (ChromaDB C++ 빌드 의존성 해결)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt-get/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "-m", "streamlit", "run", "app.py", "--server.port=8000", "--server.address=0.0.0.0"]
