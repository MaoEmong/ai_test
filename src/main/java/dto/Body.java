package dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
// 상품등록 요청 body.
public class Body {
    private String name;
    private int price;
    private int qty;
}
