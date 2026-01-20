# AI DB Operator Agent (Python)

## 개요
자연어 명령을 받아 단일 테이블(`product`)에 대한 SQL을 생성하고 실행하는 FastAPI 기반 에이전트다. `/run` 한 번으로 계획 생성과 실행을 수행하며, 클라이언트에는 자연어 `message`만 반환하도록 설계되어 있다.

## 핵심 흐름
1) 사용자 자연어 입력 수신
2) LLM이 CRUD 계획(Plan) 생성
3) SQL 생성 및 안전 확인
4) DB 실행 또는 confirm 요구
5) 자연어 메시지로 응답

## 엔드포인트
### `POST /run`
요청:
```json
{
  "text": "자연어 명령",
  "confirm": false
}
```
- `text` 필수
- `confirm` 선택(기본 false)

응답:
```json
{
  "message": "자연어 결과 메시지"
}
```
- UPDATE/DELETE는 `confirm=true` 없으면 실행되지 않음

## 응답 메시지 정책
- READ
  - 0건: "조건에 맞는 결과가 없습니다."
  - N건: "총 N건을 찾았어요. 예: (...)"
- INSERT: "N건이 추가되었습니다."
- UPDATE: "N건이 수정되었습니다."
- DELETE: "N건이 삭제되었습니다."

## 안전 규칙
- UPDATE/DELETE는 기본적으로 `confirm=true`가 필요
- DELETE는 항상 confirm 필요
- 영향 row 수가 기준치 이상이면 confirm 필요

## 모듈 구조(권장)
```
app/
  main.py            # FastAPI 엔트리포인트
  routes.py          # /run 라우트
  config.py          # 상수/설정
  models.py          # Pydantic 스키마
  sql_builder.py     # SQL 생성/검증
  llm.py             # LLM 호출/Plan 생성
  db.py              # DB 헬퍼
  formatter.py       # 자연어 응답 포맷터
```

## 최적화/개선 포인트(단기)
- SQL 빌드 중복 제거
- 기본 limit 축소(예: 50 → 20)
- DELETE 프리뷰 생략, confirm만 요구
- DB 타임아웃 추가
- 프롬프트/스키마 축소로 LLM 호출 비용 절감

## 테스트/운영 메모
- 클라이언트는 `message`만 사용
- 필터가 잘 안 잡히면 프롬프트에 한국어 예시 규칙 추가
- 요청 타임아웃 10~20초 권장

## 로그 가이드
- 요청 수신/LLM/DB/confirm/예외를 INFO/WARNING/ERROR로 기록
- 민감정보는 로그에 남기지 않음

## 문서 구성 (TASK)
- TASK01: 단기 최적화 메모
- TASK02: 모듈 분리/구조화
- TASK03: `/plan`+`/execute` → `/run` 통합 설계
- TASK04: 통합/최적화 반영 요약
- TASK05: 자연어 메시지 응답 설계
- TASK06: 테스트 결과 기록
- TASK07: 클라이언트 요청/응답 가이드
- TASK08: 서버 로그 출력 가이드
