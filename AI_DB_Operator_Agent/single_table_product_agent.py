"""
리팩터링된 app 패키지를 위한 호환 래퍼.

실행:
  uvicorn single_table_product_agent:app --reload
"""

from app.main import app
