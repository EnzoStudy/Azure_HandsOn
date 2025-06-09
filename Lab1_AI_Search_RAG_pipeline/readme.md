개인 블로그 게시물 : https://enzo.super.site/%EB%B8%94%EB%A1%9C%EA%B7%B8-%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4/azure-ai-rag-%EC%96%B4%ED%94%8C%EB%A6%AC%EC%BC%80%EC%9D%B4%EC%85%98-%EA%B0%9C%EB%B0%9C-%ED%8C%8C%EC%9D%B4%ED%94%84%EB%9D%BC%EC%9D%B8


# Azure AI RAG 솔루션 구축 워크샵

이 워크샵은 Microsoft Azure의 최신 생성형 AI 기술을 활용하여 실제 비즈니스 데이터를 기반으로 한 검색 증강 생성(Retrieval Augmented Generation, RAG) 솔루션을 직접 구축하고 실습하는 과정입니다
Azure OpenAI, Azure AI Search, Azure Storage 등 주요 클라우드 서비스를 활용해 인프라를 구성하고, 맞춤형 AI 챗봇 및 검색 서비스를 개발할 수 있습니다.

## 솔루션 아키텍처

전체 솔루션은 다음과 같은 구조로 구성됩니다

![Architecture Block diagram](https://github.com/user-attachments/assets/0aab1997-e825-46a6-ba5a-3e6ec9116322)


### 데이터 처리 파이프라인

데이터 업로드 및 저장 단계에서는 기업 데이터(예: 여행 브로셔 PDF 등)를 Azure Blob Storage에 업로드합니다
이후 Azure AI Search에서 Blob Storage의 데이터를 연결해 인덱스를 생성하고, Azure OpenAI의 임베딩 모델로 데이터를 벡터화하여 의미기반 검색이 가능하도록 구성합니다.
Azure OpenAI에서는 텍스트 임베딩 모델과 GPT모델을 각각 배포하여 데이터 벡터화와 자연어 응답 생성을 담당합니다.

### 애플리케이션 개발

Visual Studio Code 환경에서 제공된 샘플 코드를 활용해 Azure OpenAI와 AI Search를 연동하는 챗봇/검색 애플리케이션을 개발합니다.
사용자의 질문이 들어오면 AI Search가 관련 데이터를 검색하고, OpenAI가 해당 데이터를 근거로 답변을 생성하는 구조입니다.
최종적으로 사용자는 챗봇 또는 검색 인터페이스를 통해 자연어로 질문을 입력하고, 시스템은 사내 데이터에 기반한 신뢰도 높은 답변을 제공하며 사용된 데이터 출처도 함께 제시할 수 있습니다.


## 필수 Azure 서비스

### Azure OpenAI Service

GPT-4o 등 최신 LLM(대형 언어 모델)을 제공하며, REST API를 통해 자연어 처리, 텍스트 생성, 임베딩 등 다양한 AI 기능을 사용할 수 있습니다[1]. 이 서비스는 텍스트 임베딩과 자연어 응답 생성의 핵심 역할을 담당합니다.

### Azure AI Search

비정형 데이터를 색인화하고, 벡터 검색 및 시맨틱 랭킹 기능을 제공하여 고품질의 검색 서비스를 구현할 수 있습니다.
RAG 솔루션에서 사용자 질의에 관련된 문서를 효율적으로 검색하는 역할을 수행합니다.

### Azure Storage (Blob Storage)

기업 데이터(예: PDF, 문서 등)를 안전하게 저장하고, AI Search 및 OpenAI와 연동하여 데이터 소스로 활용합니다.
원본 문서들의 저장소 역할을 하며 AI Search의 데이터 소스가 됩니다.

## 단계별 구축 가이드

### Azure 리소스 생성

Azure 포털에 로그인한 후, Azure OpenAI 리소스를 먼저 생성합니다.
구독 선택 시 Azure 오픈 액세스가 승인된 구독을 선택해야 하며, 지역은 미국 동부, 미국 동부 2, 미국 북중부, 미국 남중부, 스웨덴 센트럴, 미국 서부, 미국 서부 3 중에서 선택합니다
가격 계층은 기본적으로 Standard S0 계층을 선택합니다

Azure AI Search 리소스는 Azure OpenAI와 동일한 구독 및 리소스 그룹에서 생성하며, 위치도 동일한 지역을 선택하여 네트워크 지연을 줄이고 리소스 간 연동을 원활하게 합니다.
가격 계층은 "표준(기본)"을 선택합니다.

Storage Account는 마찬가지로 동일한 구독, 리소스 그룹, 지역에서 생성하며, 주요 서비스로 Azure Blob Storage 또는 Azure Data Lake Storage Gen2를 선택합니다.
성능은 Standard, 중복성은 Locally redundant storage (LRS)를 선택합니다

### 서비스 구성 정보 수집

모든 리소스가 성공적으로 배포된 후, 각 서비스의 엔드포인트와 키 정보를 수집해야 합니다. Azure OpenAI 리소스에서는 Keys and Endpoint 페이지에서 엔드포인트와 KEY1 또는 KEY2 중 하나를 복사합니다
Azure AI Search 서비스에서는 개요 페이지의 Url 값과 Keys 페이지의 Primary admin key 값을 복사합니다


### 데이터 업로드 및 인덱스 생성

원하는 파일을 준비합니다 (PDF / Word / PPT 등)
Azure 포털의 Storage browser에서 margies-travel 컨테이너를 생성하여 PDF 브로셔 파일을 업로드합니다

AI Search에서 인덱스를 생성하기 위해 Overview 페이지에서 "Import and vectorize data"를 클릭하고 Azure Blob Storage를 데이터 소스로 선택합니다.
텍스트 벡터화 설정에서 Azure OpenAI를 선택하고 text-embedding-ada-002 모델 배포를 설정합니다.
의미론적 랭킹을 활성화하고 인덱서를 한 번 실행하도록 스케줄링한 후, Objects name prefix를 margies-index로 설정하여 인덱스를 생성합니다.

## AI 모델 배포

### Cloud Shell을 통한 모델 배포

Azure Portal에서 Cloud Shell을 열고 다음 명령어로 텍스트 임베딩 모델을 배포합니다:

```bash
az cognitiveservices account deployment create \
   -g  \
   -n  \
   --deployment-name text-embedding-ada-002 \
   --model-name text-embedding-ada-002 \
   --model-version "2"  \
   --model-format OpenAI \
   --sku-name "Standard" \
   --sku-capacity 1
```

GPT-4o 모델 배포를 위해서는 다음 명령어를 사용합니다[1]:

```bash
az cognitiveservices account deployment create \
   -g  \
   -n  \
   --deployment-name gpt-4o \
   --model-name gpt-4o \
   --model-version "2024-05-13" \
   --model-format OpenAI \
   --sku-name "Standard" \
   --sku-capacity 5
```

## 애플리케이션 개발

### 개발 환경 설정

Visual Studio Code에서 Git: Clone 명령을 실행하여 https://github.com/EnzoStudy/Azure_HandsOn.git 레포지토리를 로컬 폴더에 클론합니다.
클론이 완료되면 해당 폴더를 Visual Studio Code에서 열고, 팝업 메시지가 나오면 "Yes, I trust the authors"를 선택합니다.

프로젝트 폴더 구조는 다음과 같습니다:
```
flask-azure-ai/
├── app.py                    # 메인 Flask 애플리케이션
├── templates/
│   └── index.html           # HTML 템플릿
└── .env                     # 환경변수
```

### 필수 패키지 설치

프로젝트 디렉토리에서 다음 명령어로 필요한 패키지를 설치합니다:

```bash
cd Lab1_AI_Search_RAG_pipeline    
pip install -r requirement.txt
```

### 환경 변수 설정

.env 파일에 다음 환경변수를 설정합니다:

```bash
AZURE_OAI_ENDPOINT=https://openaiservicerag.openai.azure.com
AZURE_OAI_KEY=AaUqM8L7YdNeP0O7gFIuN79dE~~~~~~~
AZURE_OAI_DEPLOYMENT=gpt-4o
AZURE_SEARCH_ENDPOINT=https://ragpipeline8.search.windows.net
AZURE_SEARCH_KEY=Avr7vuhK6cnUmvWq6Bsn6~~~~~
AZURE_SEARCH_INDEX=margies-index
```

## 소스 코드 구조

### Flask 애플리케이션 (app.py)

메인 애플리케이션은 Flask 프레임워크를 사용하여 구현되며, Azure OpenAI 클라이언트를 초기화하고 사용자의 질문을 처리하는 라우트를 제공합니다.
사용자가 질문을 제출하면 Azure OpenAI의 채팅 완성 API를 호출하고, extra_body 파라미터를 통해 Azure Search 데이터 소스를 연결하여 RAG 기능을 구현합니다.

### 사용자 인터페이스 (index.html)

사용자 인터페이스는 반응형 웹 디자인으로 구현되어 있으며, 질문 입력창, 출처 표시 옵션, AI 답변 표시 영역으로 구성됩니다[1]. CSS는 모던한 그라데이션 디자인과 애니메이션 효과를 포함하고 있으며, 모바일 환경에서도 최적화되도록 미디어 쿼리를 사용합니다.

## 실행 방법

### 로컬 서버 실행

.env 파일에 환경변수를 올바르게 설정한 후, 터미널에서 다음 명령어를 실행합니다:

```bash
python app.py
```

애플리케이션이 성공적으로 시작되면 브라우저에서 http://localhost:5000에 접속하여 AI 챗봇 인터페이스를 사용할 수 있습니다.

## 결론

이 워크샵을 통해 구축된 RAG 솔루션은 기업의 내부 문서를 기반으로 한 지능형 검색 및 질의응답 시스템의 기초를 제공합니다. 
Azure의 관리형 AI 서비스들을 조합하여 복잡한 AI 인프라를 비교적 간단하게 구축할 수 있으며, 실제 업무 환경에서 활용 가능한 수준의 솔루션을 개발할 수 있습니다. 
향후 이 기본 구조를 바탕으로 더 복잡한 비즈니스 로직과 고도화된 UI/UX를 추가하여 엔터프라이즈급 AI 애플리케이션으로 발전시킬 수 있습니다.

<img width="434" alt="final UI" src="https://github.com/user-attachments/assets/7e51d917-b00a-4c22-8af8-cf5af2144991" />
