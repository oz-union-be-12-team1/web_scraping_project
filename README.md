# web_scraping_project

Flask와 MySQL을 기반으로 한 사용자 설문 응답 시스템입니다.  
회원가입, 질문/선택지 응답, 이미지 관리, 통계 확인 등의 기능을 제공합니다.

---

## 👥 팀원 구성

**팀장**  
- BE_12_강민규  

**팀원**  
- BE_12_김민경  
- BE_12_신정우  
- BE_12_강동욱

---

## 📁 프로젝트 구성
<pre><code>
WEB_SCRAPING_PROJECT/           # 프로젝트 루트 폴더
├── .venv/                      # 의존성 패키지를 모아두는 가상환경
├── .gitignore                  # Git에 업로드 제외할 파일 목록
├── app/                        # Flask 애플리케이션 코드 폴더
│   ├── __init__.py             # 앱 초기화 및 설정 파일
│   ├── routes/                 # 라우터 및 API 핸들러 모음
│   │   ├── __init__.py         # blueprint 등록 파일
│   │   ├── users.py            # 사용자 관련 API
│   │   ├── questions.py        # 질문 관련 API
│   │   ├── choices.py          # 선택지 관련 API
│   │   ├── answers.py          # 응답 저장 API
│   │   ├── images.py           # 이미지 등록 및 수정 API
│   │   └── stats_routes.py     # 통계 API (제공)
│   └── models.py               # SQLAlchemy 모델 정의
├── config.py                   # 데이터베이스 및 앱 설정 파일
├── requirements.txt            # 설치 패키지 목록
├── run.py                      # 개발 환경 실행용 파일
├── wsgi.py                     # 배포 환경 실행용 파일
├── scripts/                    # 배포 스크립트
│   ├── launch.sh               # Flask 실행 스크립트
│   └── terminate.sh            # Flask 종료 스크립트
└── migrations/                 # DB 마이그레이션 폴더 (자동 생성)
</code></pre>
---

## 🔧 사용 기술

- Python 3.13
- Flask, Flask-Migrate, SQLAlchemy
- MySQL (pymysql)
- Postman

---

## ✅ 주요 기능 요약

### 1. 사용자 API (`/signup`)
- 이름, 이메일, 나이대, 성별을 등록
- `Enum`으로 유효한 값만 허용 (대소문자 무관하게 처리)
- 중복 이메일 방지

### 2. 질문 & 선택지 API
- 질문 등록: `/question` (POST)
- 질문 조회: `/questions/<sqe>` (GET)
- 질문 개수: `/questions/count` (GET)
- 선택지 등록: `/choice` (POST)
- 선택지 조회: `/choices/<question_id>` (GET)

### 3. 답변 API
- 복수 선택지 응답 제출: `/submit` (POST)

```json
[
  { "user_id": 1, "choice_id": 2 },
  { "user_id": 1, "choice_id": 4 }
]