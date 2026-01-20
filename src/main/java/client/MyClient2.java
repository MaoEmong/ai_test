package client;

import com.google.gson.Gson;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.nio.charset.StandardCharsets;

public class MyClient2 {
    private static final String SERVER_URL = "http://127.0.0.1:8000/run";

    public static void main(String[] args) {
        Gson gson = new Gson();

        try (BufferedReader reader = new BufferedReader(new InputStreamReader(System.in))) {
            while (true) {
                System.out.print("자연어 명령 입력 (exit 종료): ");
                String text = reader.readLine();
                if (text == null || "exit".equalsIgnoreCase(text.trim())) {
                    break;
                }

                System.out.print("confirm 여부 (true/false): ");
                String confirmInput = reader.readLine();
                boolean confirm = Boolean.parseBoolean(confirmInput);

                RequestBody body = new RequestBody(text, confirm);
                String json = gson.toJson(body);

                String response = postJson(SERVER_URL, json);
                ResponseBody result = gson.fromJson(response, ResponseBody.class);

                System.out.println("응답: " + result.message);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    // JSON POST 요청.
    private static String postJson(String urlString, String json) throws Exception {
        URL url = new URL(urlString);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod("POST");
        conn.setRequestProperty("Content-Type", "application/json");
        conn.setDoOutput(true);

        try (OutputStream os = conn.getOutputStream()) {
            byte[] bytes = json.getBytes(StandardCharsets.UTF_8);
            os.write(bytes);
        }

        try (BufferedReader br = new BufferedReader(
            new InputStreamReader(conn.getInputStream(), StandardCharsets.UTF_8))) {
            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = br.readLine()) != null) {
                sb.append(line);
            }
            return sb.toString();
        }
    }

    // 요청 바디 DTO.
    private static class RequestBody {
        String text;
        boolean confirm;

        RequestBody(String text, boolean confirm) {
            this.text = text;
            this.confirm = confirm;
        }
    }

    // 응답 바디 DTO.
    private static class ResponseBody {
        String message;
    }
}
