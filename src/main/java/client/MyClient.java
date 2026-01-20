package client;

import com.google.gson.Gson;
import dto.Body;
import dto.QueryString;
import dto.RequestDTO;
import dto.ResponseDTO;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.Socket;

public class MyClient {
    public static void main(String[] args) {
        try {
            Socket socket = new Socket("localhost", 20000);

            BufferedReader keyBuf = new BufferedReader(new InputStreamReader(System.in));
            BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
            BufferedReader br = new BufferedReader(new InputStreamReader(socket.getInputStream()));

            Gson gson = new Gson();

            while (true) {
                // 메뉴 기반 요청 생성.
                System.out.println("1.상품목록 2.상품상세 3.상품삭제 4.상품등록");
                System.out.print("번호 선택: ");
                String menuInput = keyBuf.readLine();
                if (menuInput == null || menuInput.trim().isEmpty()) {
                    continue;
                }

                int menu = Integer.parseInt(menuInput);

                RequestDTO request = new RequestDTO();

                if (menu == 1) {
                    request.setMethod("get");
                    request.setQuerystring(null);
                    request.setBody(null);
                } else if (menu == 2) {
                    System.out.print("조회할 상품 id 입력: ");
                    int id = Integer.parseInt(keyBuf.readLine());
                    request.setMethod("get");
                    request.setQuerystring(new QueryString(id));
                    request.setBody(null);
                } else if (menu == 3) {
                    System.out.print("삭제할 상품 id 입력: ");
                    int id = Integer.parseInt(keyBuf.readLine());
                    request.setMethod("delete");
                    request.setQuerystring(new QueryString(id));
                    request.setBody(null);
                } else if (menu == 4) {
                    System.out.print("상품명 입력: ");
                    String name = keyBuf.readLine();
                    System.out.print("가격 입력: ");
                    int price = Integer.parseInt(keyBuf.readLine());
                    System.out.print("수량 입력: ");
                    int qty = Integer.parseInt(keyBuf.readLine());
                    request.setMethod("post");
                    request.setQuerystring(null);
                    request.setBody(new Body(name, price, qty));
                } else {
                    System.out.println("잘못된 입력입니다.");
                    continue;
                }

                // JSON 요청을 한 줄로 전송.
                String json = gson.toJson(request);
                bw.write(json);
                bw.write("\n");
                bw.flush();

                // 한 줄 JSON 응답 수신.
                String line = br.readLine();
                if (line == null) {
                    break;
                }

                // JSON 응답 파싱 후 사용자 친화적으로 출력.
                ResponseDTO<Object> response = gson.fromJson(line, ResponseDTO.class);
                if (!"ok".equals(response.getMsg())) {
                    System.out.println("실패: " + response.getMsg());
                    continue;
                }

                Object responseBody = response.getBody();
                if (responseBody == null) {
                    System.out.println("처리 완료");
                    continue;
                }

                if (responseBody instanceof java.util.List) {
                    // 목록 출력.
                    System.out.println("상품목록");
                    System.out.printf("%-4s %-6s %-12s %-8s %-6s%n", "No", "ID", "Name", "Price", "Qty");
                    int index = 1;
                    for (Object item : (java.util.List<?>) responseBody) {
                        java.util.Map<?, ?> map = (java.util.Map<?, ?>) item;
                        int id = toInt(map.get("id"));
                        int price = toInt(map.get("price"));
                        int qty = toInt(map.get("qty"));
                        String name = String.valueOf(map.get("name"));
                        System.out.printf(
                            "%-4d %-6d %-12s %-8d %-6d%n",
                            index,
                            id,
                            name,
                            price,
                            qty
                        );
                        index++;
                    }
                } else if (responseBody instanceof java.util.Map) {
                    // 상세 출력.
                    java.util.Map<?, ?> map = (java.util.Map<?, ?>) responseBody;
                    System.out.println("상품상세");
                    System.out.printf("%-6s %-12s %-8s %-6s%n", "ID", "Name", "Price", "Qty");
                    int id = toInt(map.get("id"));
                    int price = toInt(map.get("price"));
                    int qty = toInt(map.get("qty"));
                    String name = String.valueOf(map.get("name"));
                    System.out.printf(
                        "%-6d %-12s %-8d %-6d%n",
                        id,
                        name,
                        price,
                        qty
                    );
                } else {
                    System.out.println(responseBody);
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // Gson 숫자 타입을 int로 통일.
    private static int toInt(Object value) {
        if (value instanceof Number) {
            return ((Number) value).intValue();
        }
        return Integer.parseInt(String.valueOf(value));
    }
}
