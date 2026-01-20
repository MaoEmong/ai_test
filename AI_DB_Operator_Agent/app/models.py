"""요청/플랜용 Pydantic 스키마."""

from typing import Dict, List, Literal, Optional, Union

from pydantic import BaseModel

Intent = Literal["READ", "INSERT", "UPDATE", "DELETE"]


class WhereClause(BaseModel):
    col: Literal["id", "name", "price", "qty"]
    op: Literal["=", "!=", ">", ">=", "<", "<=", "LIKE", "IN"]
    val: Union[str, int, float, List[Union[str, int, float]]]


class Plan(BaseModel):
    intent: Intent

    # 조회(READ)
    select_cols: Optional[List[Literal["id", "name", "price", "qty"]]] = None
    order_by: Optional[Literal["id", "name", "price", "qty"]] = None
    order_dir: Optional[Literal["ASC", "DESC"]] = None
    limit: Optional[int] = None

    # 삽입/수정
    set_values: Optional[
        Dict[Literal["id", "name", "price", "qty"], Union[str, int, float, None]]
    ] = None

    # WHERE (READ/UPDATE/DELETE 공통)
    where: Optional[List[WhereClause]] = None

    # 안전장치
    needs_confirm: bool = False
    reason: str = ""


class RunRequest(BaseModel):
    text: str
    confirm: bool = False
