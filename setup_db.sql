-- PostgreSQL database setup for e-commerce application
-- Run this script as: psql postgres -f setup_db.sql

-- Create user
CREATE USER ecommerce_user WITH PASSWORD 'ecommerce_password';

-- Create database
CREATE DATABASE ecommerce_db OWNER ecommerce_user;

-- Grant privileges
GRANT ALL PRIVILEGES ON DATABASE ecommerce_db TO ecommerce_user;

-- Connect to the new database
\c ecommerce_db

-- Grant schema permissions
GRANT ALL ON SCHEMA public TO ecommerce_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO ecommerce_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO ecommerce_user;

-- Display success message
SELECT 'Database setup completed successfully!' as status;
