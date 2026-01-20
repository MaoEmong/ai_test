package server;

import java.util.List;

// 서비스 계층 계약.
public interface ProductServiceInterface {
    List<Product> findAll();
    Product findById(int id);
    int deleteById(int id);
    int save(String name, int price, int qty);
}
