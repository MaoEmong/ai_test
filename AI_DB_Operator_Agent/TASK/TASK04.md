# TASK04: 마무리 작업 정리

## 작업 개요
TASK01~TASK03 내용을 반영해 API를 단일 엔드포인트로 통합하고, 단기 최적화(기본 limit 축소, LLM 프롬프트 단순화, DB 타임아웃)를 적용했다. 변경된 흐름에 맞게 `/run` 응답 형태를 통일했다.

## 변경 사항
- `/plan`, `/execute` 제거 후 `/run` 단일 엔드포인트로 통합
- UPDATE/DELETE는 confirm이 없으면 실행하지 않고 안내 응답 반환
- DELETE는 프리뷰 없이 confirm만 요구
- 기본 limit 50 -> 20으로 축소
- LLM 프롬프트를 ASCII/간결 규칙으로 정리
- DB 커넥션 타임아웃 추가

## 코드 주석(간략)
- `app/routes.py`: confirm=false인 UPDATE/DELETE는 확인 안내만 반환, DELETE는 프리뷰 생략
- `app/db.py`: 짧은 타임아웃으로 멈춤 방지

## 파일별 변경 내용
- `app/routes.py`
  - `/run` 엔드포인트만 유지
  - confirm이 없으면 안내 응답, UPDATE만 프리뷰 생성
  - 응답을 `{plan, sql, result}` 또는 `{plan, sql, needs_confirm, message}` 형태로 통일
- `app/config.py`
  - `DEFAULT_LIMIT = 20`으로 조정
- `app/llm.py`
  - 프롬프트를 간결한 ASCII 규칙으로 재작성
- `app/db.py`
  - `connect_timeout`, `read_timeout`, `write_timeout` 추가

## 현재 사용 방법
```
POST /run
{
  "text": "price 1000 이상 상품 보여줘",
  "confirm": false
}
```

## 확인 필요 사항
- 기존 클라이언트가 `/plan`, `/execute`를 사용 중이라면 `/run`으로 변경 필요
- READ/INSERT/UPDATE/DELETE 각각 1건 이상 동작 확인 권장
