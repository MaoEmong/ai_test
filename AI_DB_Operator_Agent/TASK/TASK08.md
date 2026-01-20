# TASK08: 서버 로그 출력 가이드

## 목적
클라이언트 요청 수신, LLM 호출/응답, DB 조작 등 주요 동작 시점을 로그로 남겨 디버깅과 운영 가시성을 확보한다.

## 로그 범위
- 요청 수신: `/run` 진입 시 요청 요약
- LLM 처리: 프롬프트/입력, 응답 요약, 파싱 실패
- DB 처리: 실행 SQL 요약, 결과 건수/영향 건수
- 안전 확인: UPDATE/DELETE confirm 필요 여부 및 프리뷰 결과
- 예외 처리: 예외 타입/메시지 기록

## 로그 레벨
- INFO: 정상 흐름(요청 수신, 처리 완료)
- WARNING: confirm 필요, 비정상 입력, 부분 실패
- ERROR: 예외 발생, DB/LLM 실패

## 로그 포맷(예시, 한글)
```
[INFO] 요청 수신: text="전체 상품 조회" confirm=false
[INFO] LLM 계획: intent=READ where=0
[INFO] DB 조회: rows=3
[INFO] 응답 생성: message="총 3건을 찾았어요. 예: ..."

[WARNING] 확인 필요: intent=UPDATE preview_count=25

[ERROR] DB 오류: OperationalError (1045, "Access denied")
```

## 구현 위치(권장)
- `app/routes.py`
  - 요청 수신/응답 완료 로그
  - confirm 필요 경로 로그
- `app/llm.py`
  - LLM 호출 시작/성공/실패 로그
- `app/db.py`
  - 쿼리 실행/영향 건수 로그

## 구현 방식
- 표준 `logging` 모듈 사용
- 기본 로거 이름: `db_agent`
- 기본 로그 레벨: `INFO`

## 간단한 코드 예시
```python
import logging

logger = logging.getLogger("db_agent")

logger.info("요청 수신: text=... confirm=...")
logger.warning("확인 필요: intent=UPDATE preview_count=25")
logger.error("DB 오류: %s", err)
```

## 주의사항
- 개인정보/민감정보(비밀번호, API 키)는 로그에 기록하지 않는다.
- SQL 전체 출력이 민감할 수 있으므로 파라미터는 마스킹하거나 길이를 제한한다.
- 대량 결과는 건수만 기록하고 내용은 샘플만 남긴다.
