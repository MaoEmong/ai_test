# Task01 - 수정 진행 가이드

## 목표
Task00.md 요구사항에 맞춰 반이중 Socket 기반 JSON 상품 API 서버로 동작하도록 프로젝트를 정비한다.
코드 작성은 하지 않고, 어디를 어떻게 수정할지 절차를 정리한다.

---

## 변경 대상 요약
- `src/main/java/server/MyServer.java`: 소켓 수신, JSON 파싱, 요청 분기, 응답 작성
- `src/main/java/server/Product.java`: 상품 모델 필드 정의
- `src/main/java/dto/RequestDTO.java`: 요청 DTO 필드 정의
- `src/main/java/dto/ResponseDTO.java`: 응답 DTO 필드 정의
- `src/main/java/server/ProductServiceInterface.java`: 서비스 메서드 시그니처 정리
- `src/main/java/server/ProductService.java`: 서비스 로직 연결
- `src/main/java/server/ProductRepository.java`: SQL 처리 메서드 정의
- `src/main/java/server/DBConnection.java`: 유지 (필요 시 연결 방식만 점검)
- `src/main/java/client/MyClient.java`: 테스트 용도, 필요 시 입력 안내만 보완

---

## 수정 절차

1) 모델/DTO 구조 확정
- Product: id, name, price, qty 4개 필드를 갖는 단순 모델로 정리한다.
- RequestDTO: method, querystring, body 필드만 포함한다.
- ResponseDTO: msg, body 필드만 포함한다.
- DTO는 JSON 직렬화/역직렬화가 가능하도록 필드 접근자 규칙을 통일한다.

2) 서비스 인터페이스를 요구사항 기준으로 정리
- Task00.md에 제시된 메서드 시그니처로 통일한다.
- 현재 한글/깨진 메서드명은 ASCII 기반 이름으로 바꿔 가독성과 컴파일 안정성을 확보한다.
- 반환 타입과 예외 처리 기준을 명확히 한다(성공/실패를 msg로 표현).

3) Repository 계층 설계
- ProductRepository에 아래 4개 동작을 담당하는 메서드가 필요하다.
  - 목록 조회, 단건 조회, 등록, 삭제
- DBConnection에서 Connection을 가져와 PreparedStatement 사용을 기준으로 설계한다.
- 예외는 서비스/컨트롤러로 전달되어 msg로 변환되도록 흐름을 잡는다.

4) Service 계층 연결
- Service는 Repository의 메서드를 호출하고, 결과를 그대로 반환한다.
- 비즈니스 규칙이 필요한 경우(없는 id 삭제 등) 예외를 발생시키는 위치를 결정한다.
- Task00.md 규칙에 맞춰 성공 시 "ok", 실패 시 예외 메시지가 되도록 흐름을 정리한다.

5) MyServer의 요청 처리 흐름 확정
- ServerSocket 열기 → accept → while(true)로 요청 반복 수신 구조를 유지한다.
- 한 줄 JSON을 받아 RequestDTO로 파싱한다(Gson 사용).
- 요청 분기 기준을 method와 querystring/body 유무로 결정한다.
  - get + querystring 없음: 상품목록
  - get + querystring id 있음: 상품상세
  - delete + querystring id 있음: 상품삭제
  - post + body 있음: 상품등록
- 처리 결과를 ResponseDTO로 구성하고 JSON으로 직렬화해 한 줄로 응답한다.
- "exit" 입력 시 소켓 종료 로직을 유지한다.

6) 응답 규약 일치 확인
- 응답은 항상 msg와 body만 포함한다.
- body는 목록은 배열, 상세는 객체, 등록/삭제는 null로 맞춘다.
- 실패 시 msg에 예외 메시지를 담고 body는 null로 한다.

7) 테스트 진행 방식
- Task00.md의 요청/응답 예시를 그대로 사용해 수동 테스트를 수행한다.
- get/list, get/detail, delete, post 순으로 요청을 보내고 msg와 body 형태를 확인한다.

---

## 체크리스트
- 요청 분기 기준이 querystring 유무로만 동작하는가
- ResponseDTO 형식이 모든 경우에 동일한 구조를 유지하는가
- DB 연결/자원 해제가 누락되지 않는가
- "exit" 처리 시 서버가 정상 종료되는가
