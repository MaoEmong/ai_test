package server;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

// DB 접근 전담.
public class ProductRepository {
    private final Connection con = DBConnection.getConnection();

    public List<Product> findAll() {
        String sql = "select id, name, price, qty from product";
        List<Product> result = new ArrayList<>();
        try (PreparedStatement ps = con.prepareStatement(sql);
             ResultSet rs = ps.executeQuery()) {
            while (rs.next()) {
                // ResultSet -> Product 변환.
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
