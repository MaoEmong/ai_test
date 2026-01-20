package server;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
// 상품 모델.
public class Product {
    private int id;
    private String name;
    private int price;
    private int qty;
}
