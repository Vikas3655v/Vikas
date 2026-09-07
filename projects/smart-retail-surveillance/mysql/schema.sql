CREATE DATABASE IF NOT EXISTS smart_retail;
USE smart_retail;

CREATE TABLE IF NOT EXISTS detection_events (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    event_timestamp DATETIME NOT NULL,
    class_name VARCHAR(100) NOT NULL,
    confidence DECIMAL(6,5) NOT NULL,
    x1 DECIMAL(10,2), y1 DECIMAL(10,2),
    x2 DECIMAL(10,2), y2 DECIMAL(10,2),
    INDEX idx_event_timestamp (event_timestamp),
    INDEX idx_class_name (class_name)
);
