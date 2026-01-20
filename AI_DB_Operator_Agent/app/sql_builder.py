"""SQL 검증 및 컴파일."""

from typing import Any, List, Optional

from fastapi import HTTPException

from app.config import (
    ALLOWED_COLS,
    DEFAULT_LIMIT,
    MAX_LIMIT,
    PK_COL,
    TABLE_NAME,
)
from app.models import Plan, WhereClause


def _validate_where(where: Optional[List[WhereClause]]):
    if not where:
        return
    for w in where:
        if w.col not in ALLOWED_COLS:
            raise HTTPException(400, f"Unknown where col: {w.col}")
        if w.op == "IN" and not isinstance(w.val, list):
            raise HTTPException(400, "IN requires list value")


def _compile_where(where: Optional[List[WhereClause]]) -> tuple[str, List[Any]]:
    if not where:
        return "", []
    parts: List[str] = []
    params: List[Any] = []
    for w in where:
        if w.op == "IN":
            vals = list(w.val)  # type: ignore
            if len(vals) == 0:
                parts.append("1=0")
                continue
            placeholders = ",".join(["%s"] * len(vals))
            parts.append(f"`{w.col}` IN ({placeholders})")
            params.extend(vals)
        else:
            parts.append(f"`{w.col}` {w.op} %s")
            params.append(w.val)
    return " WHERE " + " AND ".join(parts), params


def build_sql(plan: Plan) -> tuple[str, tuple, Optional[str], Optional[tuple]]:
    """
    반환값:
      main_sql, main_params, preview_sql(선택), preview_params(선택)

    preview_sql은 UPDATE/DELETE 대상 범위 확인용(SELECT id...)이다.
    """
    _validate_where(plan.where)

    # ------------------------
    # 조회(READ)
    # ------------------------
    if plan.intent == "READ":
        cols = plan.select_cols or ["id", "name", "price", "qty"]

        limit = plan.limit if plan.limit is not None else DEFAULT_LIMIT
        try:
            limit = int(limit)
        except Exception:
            limit = DEFAULT_LIMIT
        limit = min(max(limit, 1), MAX_LIMIT)

        where_sql, where_params = _compile_where(plan.where)

        order_sql = ""
        if plan.order_by:
            order_dir = plan.order_dir or "DESC"
            order_sql = f" ORDER BY `{plan.order_by}` {order_dir}"

        select_expr = ", ".join([f"`{c}`" for c in cols])
        sql = f"SELECT {select_expr} FROM `{TABLE_NAME}`{where_sql}{order_sql} LIMIT {limit}"
        return sql, tuple(where_params), None, None

    # ------------------------
    # 삽입(INSERT)
    # ------------------------
    if plan.intent == "INSERT":
        if not plan.set_values:
            raise HTTPException(400, "INSERT requires set_values")

        cols = list(plan.set_values.keys())
        if any(c not in ALLOWED_COLS for c in cols):
            raise HTTPException(400, "INSERT has unknown column")

        col_expr = ", ".join([f"`{c}`" for c in cols])
        placeholders = ",".join(["%s"] * len(cols))
        params = tuple(plan.set_values[c] for c in cols)

        sql = f"INSERT INTO `{TABLE_NAME}` ({col_expr}) VALUES ({placeholders})"
        return sql, params, None, None

    # ------------------------
    # 수정/삭제 (WHERE 필수)
    # ------------------------
    if plan.intent in ("UPDATE", "DELETE"):
        if not plan.where or len(plan.where) == 0:
            raise HTTPException(400, f"{plan.intent} requires WHERE (blocked for safety)")

        where_sql, where_params = _compile_where(plan.where)

        preview_sql = f"SELECT `{PK_COL}` FROM `{TABLE_NAME}`{where_sql} LIMIT {MAX_LIMIT}"
        preview_params = tuple(where_params)

        if plan.intent == "UPDATE":
            if not plan.set_values:
                raise HTTPException(400, "UPDATE requires set_values")

            cols = list(plan.set_values.keys())
            if any(c not in ALLOWED_COLS for c in cols):
                raise HTTPException(400, "UPDATE has unknown column")

            set_expr = ", ".join([f"`{c}`=%s" for c in cols])
            set_params = [plan.set_values[c] for c in cols]

            sql = f"UPDATE `{TABLE_NAME}` SET {set_expr}{where_sql}"
            return sql, tuple(set_params + where_params), preview_sql, preview_params

        # 삭제(DELETE)
        sql = f"DELETE FROM `{TABLE_NAME}`{where_sql}"
        return sql, tuple(where_params), preview_sql, preview_params

    raise HTTPException(400, "Unknown intent")
