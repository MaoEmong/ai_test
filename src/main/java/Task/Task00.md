
# 반이중 Socket JSON 상품 API 서버 만들기 (Java)

## 1) 목표

TCP **ServerSocket** 기반 서버를 만든다.

클라이언트는 JSON으로 요청을 보내고, 서버는 처리 후 JSON으로 응답한다.

- 통신은 **반이중(요청 → 응답)**
- 연결 유지 + 여러 요청 처리: **while(true)** 로 반복 처리

---

## 2) DB 테이블

### `product`

- `id` (PK, int)
- `name` (varchar)
- `price` (int)
- `qty` (int)

---

## 3) 요청 규약(JSON) — 그대로 사용

```json
{
  "method":"get | post | delete",
  "querystring":{
  "id":1
  },
  "body":{
  "price":1000,
  "name":"바나나",
  "qty":10
  }
}
```

### 규칙

- `post` : **body만 있음**, querystring 없음
- `get`, `delete` : **querystring만 있음**, body 없음
- **상품목록(list)** 요청은 **querystring도 없고 body도 없음**

---

## 4) 기능 요구사항(Service 4개만)

서비스 계층은 아래 4개 기능만 제공한다.

1. **상품목록**
2. **상품상세**
3. **상품삭제**
4. **상품등록**

---

## 5) 요청 구분 규칙

이번 실습에서 GET 요청은 **모두 “product” 개념으로만 처리**한다.

즉, 이름으로 구분하지 말고 **querystring 유무로 구분**한다.

### A) 상품목록 요청 (GET)

- method = `"get"`
- querystring 없음
- body 없음

✅ 예시

```json
{
  "method":"get",
  "querystring":null,
  "body":null
}
```

---

### B) 상품상세 요청 (GET)

- method = `"get"`
- querystring에 id 존재
- body 없음

✅ 예시

```json
{
  "method":"get",
  "querystring":{
      "id" : 1
  },
  "body":null
}
```

---

### C) 상품삭제 요청 (DELETE)

- method = `"delete"`
- querystring에 id 존재
- body 없음

✅ 예시

```json
{
  "method":"delete",
  "querystring":{
      "id" : 1
  },
  "body":null
}
```

---

### D) 상품등록 요청 (POST)

- method = `"post"`
- body 존재 (name, price, qty)
- querystring 없음

✅ 예시

```json
{
  "method":"post",
  "querystring":{
      "id" : 1
  },
  "body":{"name":"바나나","price":1000,"qty":10}
}
```

---

## 6) 응답 규약(JSON) — **수정됨**

응답은 **data가 없다.** 대신 **body만 존재**한다.

그리고 성공/실패는 `msg`로만 표현한다.

### ✅ 응답 형태(항상 동일)

```json
{
"msg":"ok | (예외 메시지 문자열)",
"body": {} or []
}

```

### 규칙

- 성공이면: `"msg": "ok"`
- 실패이면: `"msg": "<예외내용>"` (예: `"msg": "id not found"` 또는 `"msg": "SQL Error"`)

---

## 7) 응답 예시

### (1) 상품목록 성공

```json
{
"msg":"ok",
"body":[
   {"id":1,"name":"사과","price":3000,"qty":5},
   {"id":2,"name":"바나나","price":1000,"qty":10}
 ]
}

```

### (2) 상품상세 성공

```json
{
"msg":"ok",
"body":{"id":2,"name":"바나나","price":1000,"qty":10}
}

```

### (3) 상품삭제 성공

```json
{
"msg":"ok",
"body":null
}

```

### (4) 상품등록 성공

```json
{
"msg":"ok",
"body":null
}

```

### (5) 실패(예외 발생)

```json
{
"msg":"id not found",
"body":null
}

```

---

## 8) 서버 아키텍처 요구사항(필수)

반드시 아래 구조로 설계한다.

```
ServerSocket(Controller 역할)
   ↓ JSON 파싱 & 요청 분기
Service (비즈니스 로직)
   ↓
Repository (SQL 담당)
   ↓
DBConnection (Connection 생성)

```

---

## 9) 구현 조건(필수)

1. 서버는 `ServerSocket` 으로 포트를 열고 대기한다.
2. 클라이언트 연결 후:
    - `while(true)`로 계속 요청을 받는다.
    - 요청 1개 처리 → 응답 1개 전송 (반이중)
3. 요청은 **한 줄 JSON**이라고 가정한다. (`readLine()`)
4. 클라이언트가 `"exit"`를 보내면 서버는 소켓을 닫고 종료한다.

---

## 10) 학생이 구현해야 할 클래스 목록(필수)

### (1) Product

- id, name, price, qty

### (2) RequestDto

- method (String)
- querystring (Map<String, Object> 또는 Map<String, Integer>)
- body (Map<String, Object>)

### (3) ResponseDto

- msg (String)
- body (Object)

### (4) ProductService

- `List<Product> findAll()`
- `Product findById(int id)`
- `int deleteById(int id)` // 성공 1, 실패 시 예외
- `int save(String name, int price, int qty)` // 생성된 id 반환

### (5) ProductRepository

- 위 서비스가 호출할 SQL 처리

### (6) DBConnection

- `Connection getConnection()`

### (7) ProductServer(main)

- ServerSocket 생성
- accept()
- while 루프
- JSON 파싱 → 요청 종류 판별 → Service 호출
-