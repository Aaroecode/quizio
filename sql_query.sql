-- Create table for SignupUser
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    termsAccepted BOOLEAN NOT NULL
);

-- Insert dummy data into signup_users
INSERT INTO users (name, email, password, gender, termsAccepted)
VALUES ('John Doe', 'john@example.com', 'password123', 'male', true);

-- Create table for Login
CREATE TABLE login (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Insert dummy data into login
INSERT INTO login (email, password)
VALUES ('john@example.com', 'password123');

-- Create table for Logout
CREATE TABLE logout (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- Insert dummy data into logout
INSERT INTO logout (email)
VALUES ('john@example.com');

-- Create table for ForgotPassword
CREATE TABLE forgot_password (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- Insert dummy data into forgot_password
INSERT INTO forgot_password (email)
VALUES ('john@example.com');

-- Create table for ResetPassword
CREATE TABLE reset_password (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    new_password VARCHAR(255) NOT NULL
);

-- Insert dummy data into reset_password
INSERT INTO reset_password (email, new_password)
VALUES ('john@example.com', 'new_password456');

-- Create table for UserProfile
CREATE TABLE user_profile (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    gender VARCHAR(10),
    bio TEXT
);

-- Insert dummy data into user_profile
INSERT INTO user_profile (name, email, gender, bio)
VALUES ('John Doe', 'john@example.com', 'male', 'This is a sample bio');
