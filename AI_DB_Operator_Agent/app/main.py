"""FastAPI 엔트리포인트."""

import logging
import sys

from fastapi import FastAPI

from app.routes import router


def _configure_logging() -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("[%(levelname)s] %(message)s"))
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(logging.INFO)
    logging.getLogger("db_agent").setLevel(logging.INFO)


_configure_logging()

app = FastAPI()
app.include_router(router)
