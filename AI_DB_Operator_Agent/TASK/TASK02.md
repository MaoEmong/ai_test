# TASK02: 코드 분할(모듈화) 정리

목표: `single_table_product_agent.py`에 몰려 있는 기능을 역할별로 분리해
읽기/수정 난이도를 낮추고 변경 범위를 줄인다. (단기 사용 기준, 과한 추상화는 피함)

## 권장 디렉터리 구조 (최소 분리)
```
app/
  main.py            # FastAPI 엔트리포인트, 라우터 등록
  config.py          # 하드코딩 설정값 모음
  models.py          # Pydantic 스키마(Plan, WhereClause 등)
  db.py              # DB 연결/쿼리 헬퍼
  sql_builder.py     # SQL 생성/검증 로직
  llm.py             # OpenAI 호출 + Plan 생성
  routes.py          # /plan, /execute 라우트
```

## 모듈별 책임
- `config.py`
  - OPENAI_API_KEY, MODEL, DB 접속정보, TABLE_NAME, ALLOWED_COLS, LIMIT 등 상수만 둔다.
- `models.py`
  - `Plan`, `WhereClause`, 요청/응답 스키마 정의만 둔다.
- `db.py`
  - `_get_conn`, `db_query`, `db_execute` 같은 DB 관련 함수만 둔다.
- `sql_builder.py`
  - `_validate_where`, `_compile_where`, `build_sql`만 둔다.
- `llm.py`
  - `client` 생성, `TABLE_PROMPT`, `llm_make_plan`만 둔다.
- `routes.py`
  - `/plan`, `/execute` 라우트 함수만 둔다.
- `main.py`
  - `FastAPI()` 생성 + `include_router`로 라우터만 연결한다.

## 분할 순서 제안 (리스크 낮은 순)
1. `models.py` 분리 (의존성 거의 없음)
2. `config.py` 분리 (상수 이동)
3. `db.py` 분리 (DB 헬퍼 이동)
4. `sql_builder.py` 분리 (SQL 로직 이동)
5. `llm.py` 분리 (OpenAI 로직 이동)
6. `routes.py` + `main.py` 분리 (최종 연결)

## 임포트 규칙 (단순 유지)
- 각 모듈은 필요한 것만 직접 import
- 상수는 `from app.config import ...`
- 타입은 `from app.models import ...`
- DB/SQL/LLM은 서로 순환 참조 없도록 한 방향으로만 의존

## 빠른 적용 예시 (코드 뼈대)
```python
# app/main.py
from fastapi import FastAPI
from app.routes import router

app = FastAPI()
app.include_router(router)
```

```python
# app/routes.py
from fastapi import APIRouter, HTTPException
from app.models import PlanRequest, ExecuteRequest
from app.llm import llm_make_plan
from app.sql_builder import build_sql
from app.db import db_query, db_execute
from app.config import CONFIRM_THRESHOLD

router = APIRouter()

@router.post("/plan")
def plan(req: PlanRequest):
    ...
```

## 체크리스트
- `uvicorn app.main:app --reload`로 실행 가능해야 한다.
- 기존 API 경로(`/plan`, `/execute`)와 응답 형식이 그대로 유지된다.
- 임포트 경로가 Windows에서도 동작하도록 패키지(`app/__init__.py`) 생성.

## 주의사항
- 단기 사용이면 과도한 추상화/DI 도입은 피한다.
- 순환 import가 생기면 모듈 책임을 다시 나누고 한쪽으로 의존을 몰아준다.
