# Task06 - 클라이언트 UI 흐름 반영 문서(학습용)

Task05의 코드 예시를 기반으로, 클라이언트가 “메뉴 선택 → 입력값 수집 → 서버 요청” 흐름으로 동작하도록 구성한다.
실제 소스 수정은 하지 않고, 문서에만 작성한다.

---

## 1) `src/main/java/client/MyClient.java` (UI + 입력 흐름 반영)

아래는 메뉴 기반 입력 UI와 요청 생성 흐름을 담은 문서용 예시다.

```java
package client;

import com.google.gson.Gson;

import java.io.*;
import java.net.Socket;
import java.util.HashMap;
import java.util.Map;

public class MyClient {
    public static void main(String[] args) {
        try {
            Socket socket = new Socket("localhost", 20000);

            BufferedReader keyBuf = new BufferedReader(new InputStreamReader(System.in));
            BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
            BufferedReader br = new BufferedReader(new InputStreamReader(socket.getInputStream()));

            Gson gson = new Gson();

            while (true) {
                System.out.println("1.상품목록 2.상품상세 3.상품삭제 4.상품등록");
                System.out.print("번호 선택: ");
                String menuInput = keyBuf.readLine();

                if (menuInput == null || menuInput.trim().isEmpty()) {
                    continue;
                }

                int menu = Integer.parseInt(menuInput);

                Map<String, Object> request = new HashMap<>();
                Map<String, Object> querystring = null;
                Map<String, Object> body = null;

                if (menu == 1) {
                    // 상품목록
                    request.put("method", "get");
                    request.put("querystring", null);
                    request.put("body", null);
                } else if (menu == 2) {
                    // 상품상세
                    System.out.print("조회할 상품 id 입력: ");
                    int id = Integer.parseInt(keyBuf.readLine());
                    querystring = new HashMap<>();
                    querystring.put("id", id);
                    request.put("method", "get");
                    request.put("querystring", querystring);
                    request.put("body", null);
                } else if (menu == 3) {
                    // 상품삭제
                    System.out.print("삭제할 상품 id 입력: ");
                    int id = Integer.parseInt(keyBuf.readLine());
                    querystring = new HashMap<>();
                    querystring.put("id", id);
                    request.put("method", "delete");
                    request.put("querystring", querystring);
                    request.put("body", null);
                } else if (menu == 4) {
                    // 상품등록
                    System.out.print("상품명 입력: ");
                    String name = keyBuf.readLine();
                    System.out.print("가격 입력: ");
                    int price = Integer.parseInt(keyBuf.readLine());
                    System.out.print("수량 입력: ");
                    int qty = Integer.parseInt(keyBuf.readLine());
                    body = new HashMap<>();
                    body.put("name", name);
                    body.put("price", price);
                    body.put("qty", qty);
                    request.put("method", "post");
                    request.put("querystring", null);
                    request.put("body", body);
                } else {
                    System.out.println("잘못된 입력입니다.");
                    continue;
                }

                String json = gson.toJson(request);
                bw.write(json);
                bw.write("\n");
                bw.flush();

                String line = br.readLine();
                System.out.println(line);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

---

## 2) 서버 측 처리 로직 영향

- 요청 구조는 Task05와 동일하며, UI 입력 방식만 변경된다.
- 서버는 `method`와 `querystring/body` 유무로 분기한다.
- 클라이언트 입력이 항상 숫자로 들어온다는 가정 하에 동작한다.

---

## 3) 요청 예시 (메뉴 기반)

### 1. 상품목록
```json
{"method":"get","querystring":null,"body":null}
```

### 2. 상품상세 (id=1)
```json
{"method":"get","querystring":{"id":1},"body":null}
```

### 3. 상품삭제 (id=1)
```json
{"method":"delete","querystring":{"id":1},"body":null}
```

### 4. 상품등록
```json
{"method":"post","querystring":null,"body":{"name":"apple","price":1000,"qty":10}}
```

---

## 정리
- 클라이언트는 실행 직후 4개 메뉴를 출력하고 숫자 입력을 받는다.
- 메뉴에 따라 추가 입력값(id, name/price/qty)을 수집한다.
- 수집된 값으로 JSON 요청을 구성해 서버로 전송한다.
