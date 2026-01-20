package server;

import com.google.gson.Gson;
import dto.Body;
import dto.QueryString;
import dto.RequestDTO;
import dto.ResponseDTO;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.ServerSocket;
import java.net.Socket;

public class MyServer {
    public static void main(String[] args) {
        ProductService service = new ProductService();
        Gson gson = new Gson();

        try (ServerSocket ss = new ServerSocket(20000);
             Socket socket = ss.accept();
             BufferedReader br = new BufferedReader(new InputStreamReader(socket.getInputStream()));
             BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()))) {

            // 단일 클라이언트 요청/응답 반복 처리.
            while (true) {
                String line = br.readLine();
                if (line == null || "exit".equals(line)) {
                    break;
                }

                ResponseDTO<Object> response;
                try {
                    RequestDTO request = gson.fromJson(line, RequestDTO.class);
                    String method = request.getMethod();
                    QueryString qs = request.getQuerystring();
                    Body body = request.getBody();

                    // method와 query/body 유무로 요청 분기.
                    if ("get".equalsIgnoreCase(method) && qs == null) {
                        response = new ResponseDTO<>("ok", service.findAll());
                    } else if ("get".equalsIgnoreCase(method) && qs != null) {
                        int id = qs.getId();
                        response = new ResponseDTO<>("ok", service.findById(id));
                    } else if ("delete".equalsIgnoreCase(method) && qs != null) {
                        int id = qs.getId();
                        service.deleteById(id);
                        response = new ResponseDTO<>("ok", null);
                    } else if ("post".equalsIgnoreCase(method) && body != null) {
                        String name = body.getName();
                        int price = body.getPrice();
                        int qty = body.getQty();
                        service.save(name, price, qty);
                        response = new ResponseDTO<>("ok", null);
                    } else {
                        response = new ResponseDTO<>("bad request", null);
                    }
                } catch (Exception e) {
                    response = new ResponseDTO<>(e.getMessage(), null);
                }

                // JSON 응답을 한 줄로 전송.
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
