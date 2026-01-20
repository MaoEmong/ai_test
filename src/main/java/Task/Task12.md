# Task12 - QueryString/Body 클래스명 사용 검토

## 질문
추가 DTO 이름을 `QueryDTO`/`ProductBodyDTO` 대신  
`QueryString`/`Body`로 단순화해서 사용할 수 있는지에 대한 정리.

---

## 결론
가능하다.  
다만 클래스명은 일반적인 의미가 강하므로 **패키지 경계와 역할 설명을 명확히** 하는 것이 중요하다.

---

## 적용 방식

### 1) 클래스명 변경
- `QueryDTO` → `QueryString`
- `ProductBodyDTO` → `Body`

### 2) 위치
- `dto` 패키지에 두되, “클라이언트/서버 요청 전용 DTO”임을 문서로 명확히 한다.

---

## 장점
- 이름이 짧아 코드가 간결해진다.
- JSON 구조(`querystring`, `body`)와 직관적으로 매칭된다.

---

## 주의사항
- `Body`는 범용 단어라 역할이 모호해질 수 있음
- 후속 과제에서 다른 Body 개념이 생기면 충돌 가능
- 패키지 경계(예: `dto.request.Body`) 또는 클래스 주석으로 용도를 고정하는 것이 안전

---

## 예시 구조(문서용)

```java
package dto;

public class QueryString {
    private int id;
}

public class Body {
    private String name;
    private int price;
    private int qty;
}
```

RequestDTO:
```
private QueryString querystring;
private Body body;
```

---

## 정리
`QueryString/Body` 이름 사용은 가능하지만,  
역할이 겹치지 않도록 패키지/주석으로 범위를 고정하는 것이 좋다.
