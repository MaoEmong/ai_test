package server;

import java.util.List;

// 서비스 계층: 비즈니스 규칙 적용.
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
            // 존재하지 않는 상품 처리.
            throw new RuntimeException("id not found");
        }
        return product;
    }

    @Override
    public int deleteById(int id) {
        int rows = repository.deleteById(id);
        if (rows == 0) {
            // 존재하지 않는 상품 처리.
            throw new RuntimeException("id not found");
        }
        return rows;
    }

    @Override
    public int save(String name, int price, int qty) {
        return repository.save(name, price, qty);
    }
}
