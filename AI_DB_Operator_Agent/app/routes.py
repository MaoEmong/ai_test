"""API 라우트."""

import logging

from fastapi import APIRouter, HTTPException

from app.config import CONFIRM_THRESHOLD
from app.db import db_execute, db_query
from app.formatter import format_confirm, format_result
from app.llm import llm_make_plan
from app.models import RunRequest
from app.sql_builder import build_sql

router = APIRouter()
logger = logging.getLogger("db_agent")


@router.post("/run")
def run(req: RunRequest):
    logger.info('요청 수신: text="%s" confirm=%s', req.text, req.confirm)
    plan_obj = llm_make_plan(req.text)
    main_sql, main_params, preview_sql, preview_params = build_sql(plan_obj)

    # UPDATE/DELETE는 confirm=false면 확인 안내만 반환한다.
    if plan_obj.intent in ("UPDATE", "DELETE") and not req.confirm:
        plan_obj.needs_confirm = True

        preview_count = None
        preview_sample = None
        # DELETE는 프리뷰 없이 confirm만 요구한다.
        if plan_obj.intent == "UPDATE" and preview_sql:
            ids = db_query(preview_sql, preview_params or ())
            preview_count = len(ids)
            preview_sample = ids[:10]
            if preview_count >= CONFIRM_THRESHOLD:
                plan_obj.needs_confirm = True

        message = format_confirm(plan_obj, preview_count, preview_sample)
        logger.warning(
            "확인 필요: intent=%s preview_count=%s",
            plan_obj.intent,
            preview_count,
        )
        return {"message": message}

    if plan_obj.intent == "READ":
        rows = db_query(main_sql, main_params)
        message = format_result(plan_obj, {"rows": rows})
        logger.info("응답 생성: intent=READ rows=%s", len(rows))
        return {"message": message}

    if plan_obj.intent == "INSERT":
        affected = db_execute(main_sql, main_params)
        message = format_result(plan_obj, {"affected_rows": affected})
        logger.info("응답 생성: intent=INSERT affected=%s", affected)
        return {"message": message}

    if plan_obj.intent in ("UPDATE", "DELETE"):
        affected = db_execute(main_sql, main_params)
        message = format_result(plan_obj, {"affected_rows": affected})
        logger.info("응답 생성: intent=%s affected=%s", plan_obj.intent, affected)
        return {"message": message}

    raise HTTPException(400, "Unknown intent")
