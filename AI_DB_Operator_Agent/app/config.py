"""
설정 상수 모음.

짧게 사용할 코드이므로 보안/환경변수는 범위에서 제외한다.
"""

# OpenAI 설정
OPENAI_API_KEY = "sk-proj-REPLACE_WITH_YOUR_KEY"
OPENAI_MODEL = "gpt-5.1"

# MySQL 설정
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "root"
MYSQL_PASS = "bitc5600!"
MYSQL_DB = "productdb"

# 테이블 스키마
TABLE_NAME = "product"
PK_COL = "id"
ALLOWED_COLS = {"id", "name", "price", "qty"}

# 제한 및 안전장치
DEFAULT_LIMIT = 20
MAX_LIMIT = 200
CONFIRM_THRESHOLD = 20
