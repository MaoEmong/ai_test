# Task08 - 클라이언트 응답 출력 개선

## 배경
현재 클라이언트는 서버에서 받은 JSON 문자열을 그대로 출력하고 있다.
학습 흐름을 더 직관적으로 만들기 위해, JSON을 파싱해 사람이 읽기 쉬운 형태로 출력하는 단계가 필요하다.

---

## 목표
- 응답 JSON을 해석해 “사용자 화면용 문장”으로 출력한다.
- 성공/실패(`msg`)와 데이터(`body`)를 분리해 명확히 보여준다.

---

## 적용 위치
`src/main/java/client/MyClient.java`

---

## 출력 방식(사용자 친화형)

1) 공통 응답 처리
- 서버 응답은 `ResponseDTO` 구조로 온다.
- `msg`가 `"ok"`이면 정상, 아니면 “실패 사유”를 보여준다.

2) `body` 출력 규칙
- `body`가 `null`이면 “처리 완료” 메시지를 출력한다.
- 목록 요청은 번호와 함께 한 줄씩 출력한다.
- 단건 요청은 라벨을 붙여 한 줄로 출력한다.

---

## 출력 예시(화면용)

### 상품목록 성공
```
상품목록
1) id=1, name=사과, price=3000, qty=5
2) id=2, name=바나나, price=1000, qty=10
```

### 상품상세 성공
```
상품상세
id=2, name=바나나, price=1000, qty=10
```

### 삭제/등록 성공
```
처리 완료
```

### 실패
```
실패: id not found
```

---

## 문서용 코드 예시 (응답 출력 변환)

아래는 응답 출력만 개선하는 예시다. 실제 소스 적용은 별도로 진행한다.

```java
// 응답 수신
String line = br.readLine();

// JSON -> ResponseDTO 파싱
ResponseDTO<Object> response = gson.fromJson(line, ResponseDTO.class);

// msg 확인
if (!"ok".equals(response.getMsg())) {
    System.out.println("실패: " + response.getMsg());
    continue;
}

Object body = response.getBody();
if (body == null) {
    System.out.println("처리 완료");
    continue;
}

// Gson은 Map/Array 형태로 파싱되므로 분기 출력
if (body instanceof java.util.List) {
    System.out.println("상품목록");
    int index = 1;
    for (Object item : (java.util.List<?>) body) {
        java.util.Map<?, ?> map = (java.util.Map<?, ?>) item;
        System.out.println(
            index + ") id=" + map.get("id") +
            ", name=" + map.get("name") +
            ", price=" + map.get("price") +
            ", qty=" + map.get("qty")
        );
        index++;
    }
} else if (body instanceof java.util.Map) {
    java.util.Map<?, ?> map = (java.util.Map<?, ?>) body;
    System.out.println("상품상세");
    System.out.println(
        "id=" + map.get("id") +
        ", name=" + map.get("name") +
        ", price=" + map.get("price") +
        ", qty=" + map.get("qty")
    );
} else {
    System.out.println(body);
}
```

---

## 정리
- JSON 그대로 출력하지 말고 화면용 문장으로 변환한다.
- 목록/단건/처리완료/실패를 구분해 보여주면 사용자가 바로 이해한다.
