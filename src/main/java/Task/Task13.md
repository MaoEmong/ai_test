# Task13 - 단일 테이블 상황에서 QueryString/Body 이름 사용 정리

## 전제
현재 프로젝트는 단일 테이블(`product`)만 다룬다.
추가 테이블 확장 계획은 없다.

---

## 결론
`QueryString` / `Body` 이름을 사용해도 문제가 거의 없다.
도메인이 하나뿐이라 의미 충돌 가능성이 낮다.

---

## 이유
- 요청 구조가 `querystring`/`body`로 고정되어 있어 이름 매칭이 직관적이다.
- 단일 테이블만 다루므로 다른 요청 Body와 혼동될 여지가 적다.
- 학습용 프로젝트에서는 간결한 이름이 이해를 돕는다.

---

## 권장 방식
- `dto` 패키지에 두고 역할을 명시한다.
- 클래스명은 아래처럼 사용한다.

```java
// dto/QueryString.java
class QueryString { int id; }

// dto/Body.java
class Body { String name; int price; int qty; }
```

---

## 정리
단일 테이블 환경이라면 `QueryString` / `Body`는 간결하고 직관적인 선택이다.
