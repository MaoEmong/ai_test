# Task02 - 파일별 수정 가이드

Task01의 절차를 기준으로 각 파일을 어떤 방식으로 수정할지 정리한다.
코드 작성은 하지 않으며, 구조와 책임을 명확히 하는 데 초점을 둔다.

---

## 1) `src/main/java/server/Product.java`
- id, name, price, qty 필드를 가진 단순 모델로 구성한다.
- 생성자/기본 생성자, getter/setter 제공 여부를 결정한다.
- 직렬화/역직렬화를 고려해 필드 접근 규칙을 통일한다.

---

## 2) `src/main/java/dto/RequestDTO.java`
- 필드: method, querystring, body만 둔다.
- querystring은 id를 담는 Map 구조로 맞춘다.
- JSON 파싱이 가능하도록 필드명과 타입을 명확히 정한다.

---

## 3) `src/main/java/dto/ResponseDTO.java`
- 필드: msg, body만 둔다.
- msg는 "ok" 또는 예외 메시지 문자열을 담는다.
- body는 리스트/객체/null 중 하나가 될 수 있도록 타입을 설정한다.

---

## 4) `src/main/java/server/ProductServiceInterface.java`
- Task00 요구사항의 4개 기능 메서드로 시그니처를 통일한다.
- 메서드명은 ASCII 기반으로 정리한다(예: findAll, findById, deleteById, save).
- 반환/예외 규칙을 문서 기준으로 명확히 한다.

---

## 5) `src/main/java/server/ProductService.java`
- Repository 메서드 호출만 담당하도록 역할을 단순화한다.
- 존재하지 않는 id 삭제/조회 시 예외 처리 위치를 결정한다.
- Task00의 응답 규칙(msg, body)과 맞물리도록 결과를 전달한다.

---

## 6) `src/main/java/server/ProductRepository.java`
- DBConnection으로 Connection을 얻어 SQL 처리를 담당한다.
- 아래 4개 동작에 대응하는 메서드를 정의한다.
  - 목록 조회, 단건 조회, 등록, 삭제
- 예외는 상위 계층에서 msg로 변환되도록 전달한다.

---

## 7) `src/main/java/server/DBConnection.java`
- 현재 연결 정보를 유지하되, 연결 생성과 예외 처리 흐름만 점검한다.
- 재사용/정리 방식(try-with-resources 등)은 필요 시 반영한다.

---

## 8) `src/main/java/server/MyServer.java`
- ServerSocket 생성 → accept → while(true) 구조는 유지한다.
- 한 줄 JSON을 RequestDTO로 파싱한다(Gson 사용).
- 요청 분기 기준은 method + querystring/body 유무로만 결정한다.
  - get + querystring 없음: 목록
  - get + querystring id 있음: 상세
  - delete + querystring id 있음: 삭제
  - post + body 있음: 등록
- ResponseDTO로 응답 구조를 구성하고 JSON 한 줄로 전송한다.
- "exit" 입력 시 소켓 종료 로직을 유지한다.

---

## 9) `src/main/java/client/MyClient.java`
- 테스트용 입력/출력 흐름만 유지한다.
- 요청/응답 예시를 붙여서 수동 테스트 시나리오를 점검한다.

---

## 확인 항목
- 응답 구조가 항상 msg/body만 포함하는가
- list/detail/delete/post 요청 분기가 규약과 일치하는가
- DB 자원 정리가 누락되지 않는가
- "exit" 처리 시 서버가 정상 종료되는가
