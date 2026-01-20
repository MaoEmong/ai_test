# TASK07: 클라이언트 요청/응답 가이드

## 개요
클라이언트는 자연어 명령을 서버의 `/run` 엔드포인트로 전송하고, 서버는 `message` 문자열만 응답한다.

## 요청 위치
- Method: POST
- URL: `http://127.0.0.1:8000/run`
- Content-Type: `application/json`
- 기본 호스트/포트: `127.0.0.1:8000` (로컬 개발 기준)

## 요청 데이터
요청 바디는 JSON이며 아래 필드를 사용한다.

### 요청 바디 (형태)
```
{
  "text": "자연어 명령",
  "confirm": false
}
```

### 필드 설명
- `text` (필수): 사용자의 자연어 명령
- `confirm` (선택): UPDATE/DELETE 실행 확인용, 기본값 `false`

## 응답 데이터
응답은 JSON이며 `message`만 포함한다.

### 응답 바디 (형태)
```
{
  "message": "자연어 결과 메시지"
}
```

## 예시
### 1) 전체 조회
요청:
```
POST /run
{
  "text": "전체 상품 조회",
  "confirm": false
}
```
응답:
```
{
  "message": "총 3건을 찾았어요. 예: (id=1, name=사과, price=1000, qty=5)"
}
```

### 2) 조건 조회
요청:
```
POST /run
{
  "text": "사과 데이터 조회",
  "confirm": false
}
```
응답:
```
{
  "message": "총 1건을 찾았어요. 예: (id=1, name=사과, price=1000, qty=5)"
}
```

### 3) UPDATE/DELETE 확인 필요
요청:
```
POST /run
{
  "text": "price 1000 이상 상품을 900으로 수정",
  "confirm": false
}
```
응답:
```
{
  "message": "총 25건이 영향을 받을 수 있어요. 상위 5건 예: (id=1, name=사과, price=1000, qty=5) confirm=true로 다시 요청해주세요."
}
```

### 4) UPDATE/DELETE 실행
요청:
```
POST /run
{
  "text": "price 1000 이상 상품을 900으로 수정",
  "confirm": true
}
```
응답:
```
{
  "message": "25건을 수정했어요."
}
```

## 주의사항
- 클라이언트는 응답에서 `message`만 사용한다.
- UPDATE/DELETE는 `confirm=true`가 없으면 실행되지 않는다.
- 오류 발생 시에도 `message`가 반환될 수 있으니 사용자에게 그대로 표시한다.

## 헤더 예시
요청 시 다음 헤더를 포함한다.
```
Content-Type: application/json
```

## 에러/상태 코드
- 200 OK: 정상 처리
- 400 Bad Request: confirm 누락/의도 불명 등 요청 오류
- 500 Internal Server Error: 서버 내부 오류(DB/LLM/파싱 등)

## 에러 응답 형식

에러 시에도 응답은 `message`를 포함하는 형태로 반환될 수 있다.
```
{
  "message": "요청을 처리하지 못했어요."
}
```

## 타임아웃/재시도 권장값
- 클라이언트 요청 타임아웃: 10~20초 권장
- 네트워크 오류나 500 에러는 최대 1회 재시도 권장
