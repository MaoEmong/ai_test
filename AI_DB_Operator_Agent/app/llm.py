"""OpenAI 플랜 생성."""

import json
import logging

from fastapi import HTTPException
from openai import OpenAI

from app.config import DEFAULT_LIMIT, MAX_LIMIT, OPENAI_API_KEY, OPENAI_MODEL, TABLE_NAME
from app.models import Plan

# Concise ASCII prompt for faster responses and fewer token errors.
TABLE_PROMPT = f"""
You generate a JSON CRUD plan for a single MySQL table.

DB:
- table: {TABLE_NAME}
- columns: id (int, PK), name (varchar), price (int), qty (int)

Rules:
- intent is one of READ, INSERT, UPDATE, DELETE
- use only this table and these columns (no joins, no other tables)
- READ: default limit={DEFAULT_LIMIT}, max limit={MAX_LIMIT}; always include limit
- UPDATE/DELETE: WHERE is required; prefer id or id IN when possible
- If a request can affect many rows, set needs_confirm=true and add a short reason
- Treat id/price/qty as numbers; name as string (use LIKE or = as needed)

Output:
- Return JSON only and follow the provided JSON schema strictly.
""".strip()


client = OpenAI(api_key=OPENAI_API_KEY)
logger = logging.getLogger("db_agent")

# 고정 JSON 스키마(LLM 응답 안정화용)
PLAN_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "intent": {"type": "string", "enum": ["READ", "INSERT", "UPDATE", "DELETE"]},
        "select_cols": {
            "anyOf": [
                {
                    "type": "array",
                    "items": {"type": "string", "enum": ["id", "name", "price", "qty"]},
                },
                {"type": "null"},
            ]
        },
        "order_by": {
            "anyOf": [
                {"type": "string", "enum": ["id", "name", "price", "qty"]},
                {"type": "null"},
            ]
        },
        "order_dir": {
            "anyOf": [
                {"type": "string", "enum": ["ASC", "DESC"]},
                {"type": "null"},
            ]
        },
        "limit": {"anyOf": [{"type": "integer"}, {"type": "null"}]},
        "set_values": {
            "anyOf": [
                {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "id": {"type": ["number", "null"]},
                        "name": {"type": ["string", "null"]},
                        "price": {"type": ["number", "null"]},
                        "qty": {"type": ["number", "null"]},
                    },
                    "required": ["id", "name", "price", "qty"],
                },
                {"type": "null"},
            ]
        },
        "where": {
            "anyOf": [
                {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "col": {
                                "type": "string",
                                "enum": ["id", "name", "price", "qty"],
                            },
                            "op": {
                                "type": "string",
                                "enum": ["=", "!=", ">", ">=", "<", "<=", "LIKE", "IN"],
                            },
                            "val": {
                                "anyOf": [
                                    {"type": "string"},
                                    {"type": "number"},
                                    {
                                        "type": "array",
                                        "items": {
                                            "anyOf": [
                                                {"type": "string"},
                                                {"type": "number"},
                                            ]
                                        },
                                    },
                                ]
                            },
                        },
                        "required": ["col", "op", "val"],
                    },
                },
                {"type": "null"},
            ]
        },
        "needs_confirm": {"type": "boolean"},
        "reason": {"type": "string"},
    },
    "required": [
        "intent",
        "select_cols",
        "order_by",
        "order_dir",
        "limit",
        "set_values",
        "where",
        "needs_confirm",
        "reason",
    ],
}


def llm_make_plan(user_text: str) -> Plan:
    schema = PLAN_SCHEMA
    logger.info('LLM 호출: text="%s"', user_text)

    resp = client.responses.create(
        model=OPENAI_MODEL,
        instructions=TABLE_PROMPT,
        input=user_text,
        text={
            "format": {
                "type": "json_schema",
                "name": "product_crud_plan",
                "schema": schema,
                "strict": True,
            }
        },
    )

    raw = resp.output_text
    try:
        data = json.loads(raw)
        plan = Plan(**data)
        logger.info("LLM 계획: intent=%s where=%s", plan.intent, len(plan.where or []))
        return plan
    except Exception as e:
        logger.error("LLM 파싱 실패: %s", e)
        raise HTTPException(500, f"Plan JSON parse failed: {e}\nraw={raw[:500]}")
