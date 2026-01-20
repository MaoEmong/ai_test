# Task11 - 방법 2 적용 계획(클라이언트 전용 DTO 분리)

## 목표
MyClient.java의 Map 기반 요청 조립을 없애고,  
`querystring`과 `body`를 전용 DTO로 분리해 가독성과 타입 안정성을 높인다.

---

## 추가 클래스(예시)

### 1) `src/main/java/dto/QueryDTO.java`
- 용도: id만 담는 querystring 전용 DTO
- 필드: `int id`

### 2) `src/main/java/dto/ProductBodyDTO.java`
- 용도: 상품등록 body 전용 DTO
- 필드: `String name`, `int price`, `int qty`

---

## 기존 DTO 수정

### `src/main/java/dto/RequestDTO.java`
- `querystring` 타입을 `QueryDTO`로 변경
- `body` 타입을 `ProductBodyDTO`로 변경
- Lombok 유지 가능

---

## 클라이언트 수정 방향

### MyClient.java
- Map을 만들지 않고 DTO를 생성해서 `RequestDTO`에 세팅
- 메뉴에 따라 아래처럼 분기

1) 상품목록
- method: `"get"`
- querystring: `null`
- body: `null`

2) 상품상세
- method: `"get"`
- querystring: `new QueryDTO(id)`
- body: `null`

3) 상품삭제
- method: `"delete"`
- querystring: `new QueryDTO(id)`
- body: `null`

4) 상품등록
- method: `"post"`
- querystring: `null`
- body: `new ProductBodyDTO(name, price, qty)`

---

## 서버 영향
서버는 RequestDTO의 `querystring`/`body` 타입 변경에 맞춰 파싱 구조를 변경해야 한다.
Gson은 DTO 타입으로 바로 매핑 가능하다.

---

## 정리
방법 2는 클래스 수가 늘어나지만,  
Map 기반 구조보다 타입 안정성과 가독성이 좋아 학습용으로 적합하다.
