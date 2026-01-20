# Task07 - 서버 코드 예시(문서용)

Task06의 클라이언트 요청 흐름을 처리하는 서버 코드 예시다.
실제 소스 수정은 하지 않고, 문서에만 작성한다.

---

## `src/main/java/server/MyServer.java`

```java
package server;

import com.google.gson.Gson;
import dto.RequestDTO;
import dto.ResponseDTO;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.Map;

public class MyServer {
    public static void main(String[] args) {
        ProductService service = new ProductService();
        Gson gson = new Gson();

        try (ServerSocket ss = new ServerSocket(20000);
             Socket socket = ss.accept();
             BufferedReader br = new BufferedReader(new InputStreamReader(socket.getInputStream()));
             BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()))) {

            while (true) {
                String line = br.readLine();
                if (line == null || "exit".equals(line)) {
                    break;
                }

                ResponseDTO<Object> response;
                try {
                    RequestDTO request = gson.fromJson(line, RequestDTO.class);
                    String method = request.getMethod();
                    Map<String, Object> qs = request.getQuerystring();
                    Map<String, Object> body = request.getBody();

                    if ("get".equalsIgnoreCase(method) && qs == null) {
                        // 상품목록
                        response = new ResponseDTO<>("ok", service.findAll());
                    } else if ("get".equalsIgnoreCase(method) && qs != null && qs.get("id") != null) {
                        // 상품상세
                        int id = ((Number) qs.get("id")).intValue();
                        response = new ResponseDTO<>("ok", service.findById(id));
                    } else if ("delete".equalsIgnoreCase(method) && qs != null && qs.get("id") != null) {
                        // 상품삭제
                        int id = ((Number) qs.get("id")).intValue();
                        service.deleteById(id);
                        response = new ResponseDTO<>("ok", null);
                    } else if ("post".equalsIgnoreCase(method) && body != null) {
                        // 상품등록
                        String name = (String) body.get("name");
                        int price = ((Number) body.get("price")).intValue();
                        int qty = ((Number) body.get("qty")).intValue();
                        service.save(name, price, qty);
                        response = new ResponseDTO<>("ok", null);
                    } else {
                        response = new ResponseDTO<>("bad request", null);
                    }
                } catch (Exception e) {
                    response = new ResponseDTO<>(e.getMessage(), null);
                }

                String json = gson.toJson(response);
                bw.write(json);
                bw.write("\n");
                bw.flush();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
```

---

## 정리
- 요청은 한 줄 JSON으로 받고, RequestDTO로 파싱한다.
- method + querystring/body 유무로 요청을 분기한다.
- 응답은 ResponseDTO(msg, body) 형태로만 반환한다.
