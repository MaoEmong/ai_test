# Task10 - 클라이언트 코드 구조 개선(문서)

## 질문 요약
MyClient.java 안의 `request`, `querystring`, `body` 같은 Map 구조를 dto로 처리할 수 있는지,  
또는 클라이언트 코드를 더 깔끔하게 최적화하는 방법이 있는지에 대한 정리.

---

## 결론
가능하다.  
`RequestDTO`/`ResponseDTO`를 직접 사용하고, **클라이언트용 입력 모델**을 분리하면 코드가 더 단순해진다.

---

## 방법 1) RequestDTO 직접 사용 (가장 단순)

### 핵심 아이디어
- Map으로 조립하지 말고 `RequestDTO`에 값을 세팅한다.
- `querystring`과 `body`는 Map으로 두되, 조립은 메서드로 캡슐화한다.

### 구조 예시(문서용)

```
RequestDTO req = new RequestDTO();
req.setMethod("get");
req.setQuerystring(null);
req.setBody(null);
```

### 장점
- JSON 구조가 DTO로 명확히 드러난다.
- Gson 직렬화/역직렬화가 자연스럽다.

### 단점
- `body`, `querystring`이 여전히 Map이라 타입 안정성은 낮다.

---

## 방법 2) 클라이언트 전용 DTO 분리 (가독성 최우선)

### 핵심 아이디어
- `querystring`과 `body`를 위한 작은 DTO를 만든다.
- 예: `QueryDTO`, `ProductBodyDTO` 등

### 구조 예시(문서용)

```
class QueryDTO { int id; }
class ProductBodyDTO { String name; int price; int qty; }
```

RequestDTO 안에는
- `querystring` → QueryDTO
- `body` → ProductBodyDTO

### 장점
- 타입 안전성 증가
- 실수 입력을 컴파일 단계에서 줄일 수 있음

### 단점
- 클래스 수가 늘어난다(학습용이면 오히려 좋을 수 있음)

---

## 방법 3) 요청 생성 메서드 분리 (가장 실용적)

### 핵심 아이디어
- MyClient 안에서 “요청 생성 로직”을 별도 메서드로 분리한다.
- UI 입력 부분과 JSON 생성 부분을 분리해 가독성을 높인다.

### 구조 예시(문서용)

```
private static RequestDTO buildListRequest() { ... }
private static RequestDTO buildDetailRequest(int id) { ... }
private static RequestDTO buildDeleteRequest(int id) { ... }
private static RequestDTO buildSaveRequest(String name, int price, int qty) { ... }
```

### 장점
- main 루프가 짧아짐
- 유지보수 쉬움

### 단점
- 메서드가 늘어나는 정도

---

## 추천 방향(학습용 기준)
1) **방법 3**으로 요청 생성 로직을 분리
2) `RequestDTO` 직접 사용
3) 필요 시 `QueryDTO`, `ProductBodyDTO` 추가

---

## 정리
Map을 그대로 써도 되지만, 학습/가독성 목적이라면 DTO 활용과 요청 생성 메서드 분리가 가장 효과적이다.
