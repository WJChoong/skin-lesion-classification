CREATE DATABASE IF NOT EXISTS skin_lesion;
USE skin_lesion;

CREATE TABLE user (
    id VARCHAR(128) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    country VARCHAR(50) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME DEFAULT NULL,
    status BOOLEAN DEFAULT TRUE
);

CREATE TABLE auth (
    id VARCHAR(128) PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    level VARCHAR(50) NOT NULL,
    user_id VARCHAR(128) NOT NULL,
    status BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME DEFAULT NULL,
    CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE
);

CREATE TABLE image (
    id VARCHAR(128) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME DEFAULT NULL,
    status BOOLEAN DEFAULT TRUE
);

CREATE TABLE category (
    id VARCHAR(128) PRIMARY KEY,
    user_id VARCHAR(128) NOT NULL,
    image_id VARCHAR(128) NOT NULL,
    category VARCHAR(100) NOT NULL,
    level VARCHAR(50) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    deleted_at DATETIME DEFAULT NULL,
    status BOOLEAN DEFAULT TRUE,
    CONSTRAINT fk_category_user_id FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE,
    CONSTRAINT fk_category_image_id FOREIGN KEY (image_id) REFERENCES Image(id) ON DELETE CASCADE
);

INSERT INTO User (id, name, email, country, status) 
VALUES ('263a4480-c9d1-4573-b278-bc6a1057478b', 'John Doe', 'choongweijie15@gmail.com', 'USA', TRUE);

INSERT INTO Auth (id, password, level, user_id, status) 
VALUES ('3b531775-6c52-4fa6-a85f-f83ff9d8611e', 'ZNDdTcPOhonRdnaqNmezVr3PcHuwtAktGi9LgyIGLwc=', '1', '263a4480-c9d1-4573-b278-bc6a1057478b', TRUE);

ALTER TABLE image 
CHANGE COLUMN name image_data JSON;