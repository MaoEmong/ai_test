# 프로젝트 개요

이 폴더에는 두 개의 학습용 프로젝트가 함께 있습니다.

1) Java Socket 상품 API 서버/클라이언트
2) Python FastAPI 기반 단일 테이블 DB 에이전트
3) Task 문서 폴더

아래는 각 프로젝트의 목적, 핵심 구조, 실행 방법을 간단히 정리한 설명입니다.

---

## 1) Java Socket 상품 API 서버/클라이언트

### 목적
TCP ServerSocket 기반의 반이중 JSON 통신으로 상품 CRUD API를 구성합니다.

### 핵심 흐름
- 클라이언트가 한 줄 JSON으로 요청을 전송합니다.
- 서버는 JSON을 파싱해 서비스/레포지토리를 통해 DB를 처리합니다.
- 응답은 항상 `msg`와 `body`만 포함합니다.

### 주요 구성
- `src/main/java/server/MyServer.java`: 소켓 수신, 요청 분기, 응답 생성
- `src/main/java/server/ProductService.java`: 비즈니스 로직
- `src/main/java/server/ProductRepository.java`: SQL 처리
- `src/main/java/server/DBConnection.java`: DB 연결
- `src/main/java/client/MyClient.java`: 메뉴 기반 요청/응답 출력
- `src/main/java/dto/*`: Request/Response/QueryString/Body DTO

### 실행 개념(요약)
1. 서버 실행 후 대기
2. 클라이언트 실행
3. 메뉴에서 상품목록/상세/삭제/등록 테스트

### DB 스키마
```sql
CREATE DATABASE productdb;

USE productdb;

CREATE TABLE IF NOT EXISTS product (
  id INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  price INT NOT NULL,
  qty INT NOT NULL,
  PRIMARY KEY (id)
);
```

---

## 2) Python FastAPI 단일 테이블 DB 에이전트

### 목적
자연어 입력을 받아 LLM이 CRUD 계획을 만들고, 안전장치를 거쳐 단일 테이블에 SQL을 수행합니다.

### 핵심 흐름
- `/run` API로 `text`와 `confirm` 입력
- LLM이 CRUD 계획(Plan)을 생성
- SQL을 컴파일하고 DB에 실행
- 결과를 한국어 메시지로 요약하여 반환

### 주요 구성
- `AI_DB_Operator_Agent/app/main.py`: FastAPI 엔트리
- `AI_DB_Operator_Agent/app/routes.py`: `/run` 라우트
- `AI_DB_Operator_Agent/app/llm.py`: LLM 계획 생성
- `AI_DB_Operator_Agent/app/sql_builder.py`: SQL 컴파일
- `AI_DB_Operator_Agent/app/db.py`: MySQL 실행
- `AI_DB_Operator_Agent/app/formatter.py`: 응답 메시지 포맷
- `AI_DB_Operator_Agent/single_table_product_agent.py`: uvicorn 실행용 래퍼

### 실행 개념(요약)
- `uvicorn single_table_product_agent:app --reload`
- `/run`에 자연어 요청을 보내고 결과 메시지를 확인

---

## 3) Task 문서 폴더

### 목적
프로젝트 요구사항과 구현 흐름을 단계별로 정리한 문서 모음입니다.

### 위치
- `src/main/java/Task/*.md`
- `AI_DB_Operator_Agent/TASK/*.md`

### 내용 요약
- 요청/응답 JSON 규약, 서버 아키텍처, 서비스 인터페이스 정의
- 파일별 수정 가이드 및 코드 예시 문서
- 클라이언트 메뉴 흐름/응답 출력 개선 가이드
- QueryString/Body DTO 적용과 변경점 정리
- Python 에이전트의 단기 최적화/운영 메모 및 개선 아이디어 정리
