# TASK03: /plan과 /execute 통합 설계 문서

목표: 현재 2단계(`/plan` → `/execute`) 흐름을 단일 엔드포인트로 통합한다.
사용자는 자연어 요청 한 번으로 계획 생성과 실행을 모두 수행한다.

## 변경 이유
- 호출이 2번이라 번거롭다.
- UI/스크립트에서 상태 관리가 필요해진다.
- 단기 사용 기준으로는 단일 호출이 더 단순하다.

## 통합 엔드포인트 제안
```
POST /run
{
  "text": "price 1000 이상 상품 보여줘",
  "confirm": false
}
```

## 동작 흐름
1. LLM이 text → Plan 생성
2. SQL 생성
3. UPDATE/DELETE이면 사전 확인 로직 수행
4. 조건이 충족되면 즉시 실행, 아니면 안내 응답 반환

## 응답 설계
### 1) 바로 실행되는 경우
```json
{
  "plan": { ... },
  "sql": "...",
  "result": {
    "rows": [ ... ]
  }
}
```

### 2) 확인이 필요한 경우(UPDATE/DELETE 위험)
```json
{
  "plan": { ... },
  "sql": "...",
  "preview": {
    "count": 25,
    "sample": [ {"id":1}, {"id":2} ]
  },
  "needs_confirm": true,
  "message": "confirm=true로 재요청 필요"
}
```

## 요청 필드 정책
- `text`: 필수
- `confirm`: 선택 (기본 false)

## 안전 기준(현행 유지)
- UPDATE/DELETE는 기본적으로 `confirm=true`가 필요
- DELETE는 항상 `confirm=true`
- 대상 row 수가 `CONFIRM_THRESHOLD` 이상이면 confirm 필요

## 코드 변경 포인트
- `app/routes.py`
  - `/plan`, `/execute` 제거
  - `/run` 추가
- `app/models.py`
  - `PlanRequest`, `ExecuteRequest` 제거 또는 통합 요청 모델로 대체
- `app/sql_builder.py`, `app/llm.py`, `app/db.py`
  - 로직은 재사용, 호출 흐름만 변경

## 간단한 의사코드
```python
@router.post("/run")
def run(req: RunRequest):
    plan = llm_make_plan(req.text)
    sql, params, preview_sql, preview_params = build_sql(plan)

    if plan.intent in ("UPDATE", "DELETE"):
        if not req.confirm:
            # 프리뷰 확인 후 needs_confirm 응답
            ...
        # confirm true이면 실행
        ...
    else:
        # READ/INSERT 즉시 실행
        ...
```

## 마이그레이션 체크리스트
- 기존 클라이언트가 `/plan`, `/execute`를 쓰고 있다면 업데이트 필요
- 테스트: READ/INSERT/UPDATE/DELETE 각각 1건 이상 확인