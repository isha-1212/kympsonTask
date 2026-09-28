CREATE DATABASE IF NOT EXISTS kypson_intern;
USE kypson_intern;

CREATE TABLE products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(80) NOT NULL,
    unit VARCHAR(20) NOT NULL
);

CREATE TABLE rfqs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT NOT NULL,
    buyer_name VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    delivery_city VARCHAR(80) NOT NULL,
    notes VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id)
);

CREATE TABLE quotes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rfq_id INT NOT NULL,
    supplier_name VARCHAR(100) NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    delivery_days INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (rfq_id) REFERENCES rfqs(id)
);

INSERT INTO products (name, category, unit) VALUES
('Corrugated Boxes', 'Corrugated', 'pcs'),
('Plastic Bottles', 'Plastic', 'pcs'),
('BOPP Bags', 'Flexible', 'pcs'),
('Woven PP Sacks', 'Woven', 'pcs'),
('Shrink Film', 'Flexible', 'kg');