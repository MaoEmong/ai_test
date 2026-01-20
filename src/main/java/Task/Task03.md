# Task03 - 파일별 코드 추가 지침

각 파일에 “무슨 코드 요소를 추가해야 하는지”를 구체적으로 정리한다.
실제 코드 본문은 작성하지 않고, 추가해야 할 구성요소와 흐름만 제시한다.

---

## 1) `src/main/java/server/Product.java`
- 필드 선언: `id`, `name`, `price`, `qty`
- 생성자: 기본 생성자 + 전체 필드 생성자
- 접근자: getter/setter 또는 Lombok 사용 여부 결정
- toString 필요 시 추가(디버깅 용도)

---

## 2) `src/main/java/dto/RequestDTO.java`
- 필드 선언: `method`, `querystring`, `body`
- 타입:
  - `method`: String
  - `querystring`: Map 형태(예: `Map<String, Object>` 또는 `Map<String, Integer>`)
  - `body`: Map 형태(예: `Map<String, Object>`)
- 기본 생성자 + getter/setter 추가
- JSON 파싱을 위한 필드명 일치 확인

---

## 3) `src/main/java/dto/ResponseDTO.java`
- 필드 선언: `msg`, `body`
- 생성자: 기본 생성자 + 필드 생성자
- getter/setter 추가
- body 타입은 제네릭 또는 Object로 두어 목록/단건/null 모두 수용

---

## 4) `src/main/java/server/ProductServiceInterface.java`
- 메서드 시그니처 4개 추가(ASCII 이름 권장)
  - 목록 조회: `List<Product>`
  - 단건 조회: `Product`
  - 삭제: 성공/실패 표현을 위한 int 또는 void + 예외
  - 등록: 생성된 id를 반환하도록 int

---

## 5) `src/main/java/server/ProductService.java`
- Repository 필드 선언 및 생성
- 각 메서드에 Repository 호출 코드 추가
- 예외 발생 시 그대로 던지거나 msg로 변환할 기준 결정
- 삭제/조회 시 id 미존재 처리 흐름 추가

---

## 6) `src/main/java/server/ProductRepository.java`
- Connection 사용을 위한 필드 또는 메서드 추가
- SQL 실행 메서드 4개 추가
  - `findAll`: ResultSet → List<Product> 변환 로직
  - `findById`: ResultSet → Product 변환 로직
  - `save`: insert 후 생성 id 반환 로직
  - `deleteById`: delete 결과 row count 반환 로직
- PreparedStatement 사용 및 자원 해제 흐름 포함

---

## 7) `src/main/java/server/DBConnection.java`
- 기존 연결 코드 유지
- 필요 시 try/catch 로깅 강화 또는 예외 전파 방식 추가

---

## 8) `src/main/java/server/MyServer.java`
- Gson 인스턴스 생성 코드 추가
- 입력 라인 null/exit 처리 분기 코드 추가
- 요청 파싱 → RequestDTO 변환 코드 추가
- 분기 처리 로직 추가:
  - get + querystring 없음 → service.findAll
  - get + querystring id → service.findById
  - delete + querystring id → service.deleteById
  - post + body → service.save
- ResponseDTO 생성 및 JSON 직렬화 코드 추가
- 응답 write + flush + 개행 처리
- 예외 발생 시 msg에 예외 메시지를 넣어 응답하는 처리 추가

---

## 9) `src/main/java/client/MyClient.java`
- 테스트용 JSON 요청 예시를 주석 또는 출력 안내로 추가
- 응답 수신 후 콘솔 출력 흐름 유지

---

## 공통 주의사항
- 모든 문자열 리터럴은 ASCII로 유지(필요 시 한국어는 주석으로 제한)
- JSON 요청/응답은 한 줄로 송수신
- 성공/실패는 ResponseDTO.msg로만 구분
