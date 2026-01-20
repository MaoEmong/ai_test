# Task14 - QueryString/Body 적용 시 클라이언트·서버 변경점

## 전제
단일 테이블 프로젝트로 진행하며, 요청 DTO 이름을 `QueryString`/`Body`로 사용한다.
RequestDTO의 `querystring`과 `body` 타입을 DTO로 치환한다.

---

## 추가 클래스

1) `src/main/java/dto/QueryString.java`
- 필드: `int id`
- 용도: 상세/삭제 요청에서 id 전달

2) `src/main/java/dto/Body.java`
- 필드: `String name`, `int price`, `int qty`
- 용도: 상품등록 요청 body 전달

---

## 클라이언트 변경점 (`src/main/java/client/MyClient.java`)

1) Map 기반 요청 조립 제거
- `Map<String, Object>` 사용을 없앤다.
- 요청 생성 시 `RequestDTO`, `QueryString`, `Body`를 직접 생성한다.

2) 메뉴별 요청 생성 방식 변경
- 상품목록
  - method: `"get"`
  - querystring: `null`
  - body: `null`
- 상품상세
  - method: `"get"`
  - querystring: `new QueryString(id)`
  - body: `null`
- 상품삭제
  - method: `"delete"`
  - querystring: `new QueryString(id)`
  - body: `null`
- 상품등록
  - method: `"post"`
  - querystring: `null`
  - body: `new Body(name, price, qty)`

3) 직렬화
- Gson으로 `RequestDTO` 자체를 JSON으로 직렬화한다.

---

## 서버 변경점 (`src/main/java/server/MyServer.java`)

1) RequestDTO 파싱 후 접근 방식 변경
- 기존: `Map<String, Object> qs = request.getQuerystring();`
- 변경: `QueryString qs = request.getQuerystring();`
- 기존: `Map<String, Object> body = request.getBody();`
- 변경: `Body body = request.getBody();`

2) id 접근 변경
- 기존: `((Number) qs.get("id")).intValue()`
- 변경: `qs.getId()`

3) body 접근 변경
- 기존: `(String) body.get("name")`, `((Number) body.get("price")).intValue()`
- 변경: `body.getName()`, `body.getPrice()`, `body.getQty()`

---

## RequestDTO 변경점 (`src/main/java/dto/RequestDTO.java`)

- `querystring` 타입을 `QueryString`으로 변경
- `body` 타입을 `Body`로 변경
- Lombok 사용 시 getter/setter 자동 생성

---

## 정리
Map 기반 요청 조립/파싱을 제거하고 DTO로 직접 통신하므로  
클라이언트·서버 코드가 더 단순해지고 타입 안정성이 개선된다.
