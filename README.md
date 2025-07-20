# web_scraping_project

Flask와 MySQL을 기반으로 한 사용자 설문 응답 시스템입니다.  
회원가입, 질문/선택지 응답, 이미지 관리, 통계 확인 등의 기능을 제공합니다.

팀장
BE_12_강민규
팀원
BE_12_김민경
BE_12_신정우
BE_12_강동욱


---

## 📁 프로젝트 구성
WEB_SCRAPING_PROJECT/           # 프로젝트 폴더
├── .venv                       # 의존성 패키지를 모아두는 가상환경
├── .gitignore                  # github에 올리지 않을 파일들을 관리
├── app/                        # Flask 애플리케이션 코드 폴더
│   ├── __init__.py(제공)        # 앱 초기화 및 설정 파일
│   ├── routes/                 # view 및 route 정의
│   │   ├── __init__.py         # routes의 blueprint 관리 파일
│   │   ├── stats_routes.py(제공)# answers 통계 관련 파일
│   │   ├── users.py            # users 테이블 관련 파일
│   │   ├── questions.py        # quetions 테이블 관련
│   │   ├── choices.py          # choices 테이블 관련
│   │   ├── images.py           # images 테이블 관련
│   │   └── answers.py          # answers 테이블 관련
│   ├── models.py               # SQLAlchemy 모델 정의
├── scripts/(제공)               # 배포 시 사용할 script 파일들
├── launch.sh(제공)              # 배포 환경에서 flask를 실행하기 위한 script
├── terminate.sh(제공)           # 배포 환경에서 flask를 종료하기 위한 script
├── config.py(제공)              # Flask 및 데이터베이스 설정 파일
├── requirements.txt(제공)       # 필요한 Python 패키지 목록
├── run.py(제공)                 # 개발환경에서 테스트 하는 실행 파일
├── wsgi.py(제공)                # 배포환경에서의 실행 파일
└── migrations/(자동 생성)        # Flask-Migrate를 위한 DB 마이그레이션 파일
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