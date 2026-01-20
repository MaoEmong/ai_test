# Task04 - 수정된 코드 예시(문서용)

주의: 아래는 Task03 기준으로 "실제 코드를 수정했을 때"의 예시를 문서로 정리한 것이다.
프로젝트의 실제 소스 파일을 수정하지 말고, 이 문서에만 작성한다.

---

## 1) `src/main/java/server/Product.java`

```java
package server;

public class Product {
    private int id;
    private String name;
    private int price;
    private int qty;

    public Product() {
    }

    public Product(int id, String name, int price, int qty) {
        this.id = id;
        this.name = name;
        this.price = price;
        this.qty = qty;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getPrice() {
        return price;
    }

    public void setPrice(int price) {
        this.price = price;
    }

    public int getQty() {
        return qty;
    }

    public void setQty(int qty) {
        this.qty = qty;
    }
}
```

---

## 2) `src/main/java/dto/RequestDTO.java`

```java
package dto;

import java.util.Map;

public class RequestDTO {
    private String method;
    private Map<String, Object> querystring;
    private Map<String, Object> body;

    public RequestDTO() {
    }

    public String getMethod() {
        return method;
    }

    public void setMethod(String method) {
        this.method = method;
    }

    public Map<String, Object> getQuerystring() {
        return querystring;
    }

    public void setQuerystring(Map<String, Object> querystring) {
        this.querystring = querystring;
    }

    public Map<String, Object> getBody() {
        return body;
    }

    public void setBody(Map<String, Object> body) {
        this.body = body;
    }
}
```

---

## 3) `src/main/java/dto/ResponseDTO.java`

```java
package dto;

public class ResponseDTO<T> {
    private String msg;
    private T body;

    public ResponseDTO() {
    }

    public ResponseDTO(String msg, T body) {
        this.msg = msg;
        this.body = body;
    }

    public String getMsg() {
        return msg;
    }

    public void setMsg(String msg) {
        this.msg = msg;
    }

    public T getBody() {
        return body;
    }

    public void setBody(T body) {
        this.body = body;
    }
}
```

---

## 4) `src/main/java/server/ProductServiceInterface.java`

```java
package server;

import java.util.List;

public interface ProductServiceInterface {
    List<Product> findAll();
    Product findById(int id);
    int deleteById(int id);
    int save(String name, int price, int qty);
}
```

---

## 5) `src/main/java/server/ProductService.java`

```java
package server;

import java.util.List;

public class ProductService implements ProductServiceInterface {
    private final ProductRepository repository = new ProductRepository();

    @Override
    public List<Product> findAll() {
        return repository.findAll();
    }

    @Override
    public Product findById(int id) {
        Product product = repository.findById(id);
        if (product == null) {
            throw new RuntimeException("id not found");
        }
        return product;
    }

    @Override
    public int deleteById(int id) {
        int rows = repository.deleteById(id);
        if (rows == 0) {
            throw new RuntimeException("id not found");
        }
        return rows;
    }

    @Override
    public int save(String name, int price, int qty) {
        return repository.save(name, price, qty);
    }
}
```

---

## 6) `src/main/java/server/ProductRepository.java`

```java
package server;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class ProductRepository {
    private final Connection con = DBConnection.getConnection();

    public List<Product> findAll() {
        String sql = "select id, name, price, qty from product";
        List<Product> result = new ArrayList<>();
        try (PreparedStatement ps = con.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                Product p = new Product(
                    rs.getInt("id"),
                    rs.getString("name"),
                    rs.getInt("price"),
                    rs.getInt("qty")
                );
                result.add(p);
            }
        } catch (SQLException e) {
            throw new RuntimeException("SQL Error");
        }
        return result;
    }

    public Product findById(int id) {
        String sql = "select id, name, price, qty from product where id = ?";
        try (PreparedStatement ps = con.prepareStatement(sql)) {
            ps.setInt(1, id);
            try (ResultSet rs = ps.executeQuery()) {
                if (rs.next()) {
                    return new Product(
                        rs.getInt("id"),
                        rs.getString("name"),
                        rs.getInt("price"),
                        rs.getInt("qty")
                    );
                }
            }
        } catch (SQLException e) {
            throw new RuntimeException("SQL Error");
        }
        return null;
    }

    public int save(String name, int price, int qty) {
        String sql = "insert into product(name, price, qty) values(?, ?, ?)";
        try (PreparedStatement ps = con.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {
            ps.setString(1, name);
            ps.setInt(2, price);
            ps.setInt(3, qty);
            ps.executeUpdate();
            try (ResultSet rs = ps.getGeneratedKeys()) {
                if (rs.next()) {
                    return rs.getInt(1);
                }
            }
        } catch (SQLException e) {
            throw new RuntimeException("SQL Error");
        }
        return 0;
    }

    public int deleteById(int id) {
        String sql = "delete from product where id = ?";
        try (PreparedStatement ps = con.prepareStatement(sql)) {
            ps.setInt(1, id);
            return ps.executeUpdate();
        } catch (SQLException e) {
            throw new RuntimeException("SQL Error");
        }
    }
}
```

---

## 7) `src/main/java/server/DBConnection.java`

```java
package server;

import java.sql.Connection;
import java.sql.DriverManager;

public class DBConnection {
    public static Connection getConnection() {
        String url = "jdbc:mysql://localhost:3306/productdb";
        String username = "root";
        String password = "bitc5600!";

        try {
            Class.forName("com.mysql.cj.jdbc.Driver");
            return DriverManager.getConnection(url, username, password);
        } catch (Exception e) {
            throw new RuntimeException("DB connect fail");
        }
    }
}
```

---

## 8) `src/main/java/server/MyServer.java`

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
                        response = new ResponseDTO<>("ok", service.findAll());
                    } else if ("get".equalsIgnoreCase(method) && qs != null && qs.get("id") != null) {
                        int id = ((Number) qs.get("id")).intValue();
                        response = new ResponseDTO<>("ok", service.findById(id));
                    } else if ("delete".equalsIgnoreCase(method) && qs != null && qs.get("id") != null) {
                        int id = ((Number) qs.get("id")).intValue();
                        service.deleteById(id);
                        response = new ResponseDTO<>("ok", null);
                    } else if ("post".equalsIgnoreCase(method) && body != null) {
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

## 9) `src/main/java/client/MyClient.java`

```java
package client;

import java.io.*;
import java.net.Socket;

public class MyClient {
    public static void main(String[] args) {
        try {
            Socket socket = new Socket("localhost", 20000);

            BufferedReader keyBuf = new BufferedReader(new InputStreamReader(System.in));
            BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
            BufferedReader br = new BufferedReader(new InputStreamReader(socket.getInputStream()));

            // Example:
            // {"method":"get","querystring":null,"body":null}
            // {"method":"get","querystring":{"id":1},"body":null}
            // {"method":"delete","querystring":{"id":1},"body":null}
            // {"method":"post","querystring":null,"body":{"name":"apple","price":1000,"qty":10}}

            while (true) {
                String keyboardData = keyBuf.readLine();
                bw.write(keyboardData);
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

## 참고
- 실제 코드 반영 시, 현재 프로젝트의 패키지/의존성과 일치하는지 확인한다.
- 한국어 예외 메시지가 필요하다면 msg 규약을 깨지 않는 선에서 조정한다.
