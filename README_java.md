# Java Socket JSON 상품 API (prodapp)

## 개요
TCP ServerSocket 기반의 반이중(요청 → 응답) JSON 상품 API 서버/클라이언트 예제다. 클라이언트는 한 줄 JSON 요청을 보내고 서버는 처리 결과를 JSON으로 응답한다. 요청 분기는 method + querystring/body 유무로만 결정된다.

## 기능 범위
- 상품목록 조회
- 상품상세 조회
- 상품삭제
- 상품등록

## 요청 규약 (JSON)
```json
{
  "method": "get | post | delete",
  "querystring": { "id": 1 },
  "body": { "name": "바나나", "price": 1000, "qty": 10 }
}
```
- `post`: body만 사용
- `get`, `delete`: querystring만 사용
- 목록 요청: querystring/body 모두 없음

## 응답 규약 (JSON)
```json
{
  "msg": "ok | (예외 메시지)",
  "body": {} or [] or null
}
```
- 성공: `msg = "ok"`
- 실패: `msg = "<예외 메시지>"`, `body = null`

## 아키텍처
```
ServerSocket(Controller)
  -> Service
    -> Repository
      -> DBConnection
```

## 주요 클래스
- `server/Product`: 상품 모델(id, name, price, qty)
- `dto/RequestDTO`: 요청 DTO(method, querystring, body)
- `dto/ResponseDTO`: 응답 DTO(msg, body)
- `server/ProductServiceInterface`/`ProductService`: 4개 기능 제공
- `server/ProductRepository`: DB CRUD
- `server/DBConnection`: JDBC 연결
- `server/MyServer`: 요청 수신, 분기, 응답 전송
- `client/MyClient`: 메뉴 입력, 요청 생성, 응답 출력

## 클라이언트 흐름
- 메뉴 선택 → 입력값 수집 → JSON 요청 전송
- 응답 JSON은 파싱 후 사람이 읽기 쉬운 문장으로 출력(목록/상세/완료/실패 구분)

## DTO 구조 개선 옵션
- Map 기반 `querystring`/`body`를 DTO로 분리 가능
- 단일 테이블 환경에서는 `QueryString`/`Body` 이름 사용도 가능
- 분리 시 클라이언트/서버 모두 DTO 기반으로 직렬화/파싱

## 라이브러리
- MySQL Connector/J (mysql-connector-java)
- Gson
- Lombok

## 문서 구성 (Taskxx)
- Task00: 요구사항 및 규약
- Task01~03: 수정 절차/파일별 가이드
- Task04~07: 문서용 코드 예시 및 클라이언트/서버 흐름
- Task08: 응답 출력 가독성 개선
- Task10~14: DTO 분리 및 QueryString/Body 적용 정리
- Task09/15: 진행 이력 요약
