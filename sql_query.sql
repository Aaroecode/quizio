-- Create table for SignupUser
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    gender VARCHAR(10) NOT NULL,
    termsAccepted BOOLEAN NOT NULL
    profilePicture VARCHAR(80) DEFAULT 'https://i.sstatic.net/l60Hf.png',
    bio VARCHAR(255) DEFAULT NONE,
    updatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

CREATE TABLE faq (questionNumber int(3), question varchar(255), questionDescription VARCHAR(300), solution varchar(5000))

CREATE TABLE ticket (ticketId int(5) SERIAL PRIMARY KEY, 
    userId, issueDescription varchar(3000), 
    submittedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP)


CREATE TABLE settings(
    id SERIAL PRIMARY KEY, 
    email VARCHAR(255) UNIQUE NOT NULL, 
    password VARCHAR(255) NOT NULL,  
    notifications_enabled BOOLEAN DEFAULT TRUE, 
    privacy_settings TEXT DEFAULT 'public',  
    id_type VARCHAR(50),  
    id_document TEXT,  
    created_at TIMESTAMP DEFAULT NOW(),  
    updated_at TIMESTAMP DEFAULT NOW()  
);


CREATE INDEX idx_users_email ON users (email);
INSERT INTO users (email, password, notifications_enabled, privacy_settings, id_type, id_document)
VALUES ('john.doe@example.com', 'password', TRUE, 'public', 'passport', '123456789')

CREATE TABLE rewards(
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    referral_rewards INTEGER DEFAULT 0,  -- Rewards points for referrals
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Table for referral invites
CREATE TABLE referral_invites (
    id SERIAL PRIMARY KEY,
    referrer_id INT REFERENCES users(id),
    invitee_email VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Table for user follows (follower -> followee)
CREATE TABLE user_follows(
    id SERIAL PRIMARY KEY,
    follower_id INT REFERENCES users(id),
    followee_id INT REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes to speed up the queries
CREATE INDEX idx_referrer_id ON referral_invites (referrer_id);
CREATE INDEX idx_follower_followee ON user_follows (follower_id, followee_id);


INSERT INTO users (email, password, referral_rewards)
VALUES ('john@example.com', 10);

INSERT INTO referral_invites (referrer_id, invitee_email)
VALUES(1, 'invitee1@example.com');

INSERT INTO user_follows (follower_id, followee_id)
VALUES (1, 2);