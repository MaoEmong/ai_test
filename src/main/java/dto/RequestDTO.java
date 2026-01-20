package dto;

import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
// 클라이언트 요청 DTO.
public class RequestDTO {
    private String method;
    private QueryString querystring;
    private Body body;
}
