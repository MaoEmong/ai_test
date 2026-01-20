"""DB 결과를 한국어 메시지로 요약."""

from typing import Any, Dict, List, Optional

from app.models import Plan

SAMPLE_ROWS = 5


def _format_row(row: Dict[str, Any]) -> str:
    items = [f"{k}={row[k]}" for k in sorted(row.keys())]
    return "(" + ", ".join(items) + ")"


def format_result(plan: Plan, result: Dict[str, Any]) -> str:
    if plan.intent == "READ":
        rows: List[Dict[str, Any]] = result.get("rows", []) or []
        if not rows:
            return "조건에 맞는 결과가 없어요."

        count = len(rows)
        sample = rows[:SAMPLE_ROWS]
        sample_text = ", ".join(_format_row(r) for r in sample)

        if count > SAMPLE_ROWS:
            return f"총 {count}건을 찾았어요. 상위 {SAMPLE_ROWS}건만 보여드릴게요: {sample_text}"
        return f"총 {count}건을 찾았어요. 예: {sample_text}"

    affected = result.get("affected_rows")
    if plan.intent == "INSERT":
        return f"{affected}건을 추가했어요."
    if plan.intent == "UPDATE":
        return f"{affected}건을 수정했어요."
    if plan.intent == "DELETE":
        return f"{affected}건을 삭제했어요."

    return "요청을 처리하지 못했어요."


def format_confirm(
    plan: Plan, preview_count: Optional[int], preview_sample: Optional[List[Dict[str, Any]]]
) -> str:
    if plan.intent == "DELETE":
        return "삭제 작업은 안전을 위해 confirm=true로 다시 요청해주세요."

    if preview_count is None:
        return "안전을 위해 confirm=true로 다시 요청해주세요."

    sample = preview_sample or []
    sample_text = ", ".join(_format_row(r) for r in sample)
    if preview_count > SAMPLE_ROWS and sample_text:
        return (
            f"총 {preview_count}건이 영향을 받을 수 있어요. "
            f"상위 {SAMPLE_ROWS}건 예: {sample_text} confirm=true로 다시 요청해주세요."
        )
    if sample_text:
        return (
            f"총 {preview_count}건이 영향을 받을 수 있어요. "
            f"예: {sample_text} confirm=true로 다시 요청해주세요."
        )
    return f"총 {preview_count}건이 영향을 받을 수 있어요. confirm=true로 다시 요청해주세요."
