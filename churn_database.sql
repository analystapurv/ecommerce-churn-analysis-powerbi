CREATE DATABASE ecommerce_db;
USE ecommerce_db;

CREATE TABLE customer_churn (
    customer_id INT PRIMARY KEY,
    age INT,
    gender VARCHAR(50),
    tenure_months INT,
    total_spend_inr DECIMAL(10, 2),
    num_support_tickets INT,
    last_order_days_ago INT,
    churn_status VARCHAR(50)
);

SELECT * FROM customer_churn;

SELECT COUNT(*) FROM customer_churn;


SELECT 
    churn_status,
    COUNT(customer_id) AS total_customers,
    ROUND(SUM(total_spend_inr), 2) AS total_revenue_inr,
    ROUND(AVG(num_support_tickets), 2) AS avg_support_tickets
FROM customer_churn
GROUP BY churn_status;