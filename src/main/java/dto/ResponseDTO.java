package dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
// 서버 응답 DTO.
public class ResponseDTO<T> {
    private String msg;
    private T body;
}
