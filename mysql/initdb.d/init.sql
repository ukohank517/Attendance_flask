CREATE TABLE `event` (
    event_id        VARCHAR(100) UNIQUE NOT NULL,
    event_name      VARCHAR(100)        NOT NULL,
    organization_id VARCHAR(100)        NOT NULL DEFAULT 'unknown',    
    pswd            VARCHAR(100)        NOT NULL,
    ticket_num      INT                 NOT NULL,
    event_date      DATETIME(6)         NOT NULL,
    public_date     DATETIME(6)         NOT NULL,
    version         INT                 NOT NULL,
    created_at      DATETIME(6)         NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at      DATETIME(6)         NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    deleted         BOOLEAN             NOT NULL DEFAULT FALSE,
    PRIMARY KEY (organization_id)
);

CREATE TABLE `ticket` (
    ticket_id       INT          NOT NULL,
    event_id        VARCHAR(50)  NOT NULL,
    name            VARCHAR(100) NOT NULL,
    phone_number    VARCHAR(50)  NOT NULL,
    email           VARCHAR(100) NOT NULL,
    family_id       VARCHAR(50)  NOT NULL,
    comment         VARCHAR(250) NOT NULL,
    memo            VARCHAR(250) NOT NULL,
    version         INT          NOT NULL,
    created_at      DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at      DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    deleted         BOOLEAN      NOT NULL DEFAULT FALSE,
    PRIMARY KEY (ticket_id, organization_id),
    FOREIGN KEY (organization_id) REFERENCES organization(organization_id)
);

CREATE TABLE `personal_info` (
    mail_address VARCHAR(100) NOT NULL,
    sex VARCHAR(6) NOT NULL,
    age INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    prefecture VARCHAR(50) NOT NULL,
    createdAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updatedAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (mail_address)
);

INSERT INTO `personal_info` (mail_address, sex, age, name, prefecture, createdAt, updatedAt)
VALUES
('hoge1_1@gmail.com', 'male',   18, 'ichirou1' , 'tokyo', current_timestamp(), current_timestamp()),
('hoge2@gmail.com', 'male',   23, 'zirou2', 'osaka', current_timestamp(), current_timestamp()),
('hoge3_3@gmail.com', 'male',   31, 'saburou', 'tokyo', current_timestamp(), current_timestamp()),
('hoge4@gmail.com', 'female', 29, 'itiko', 'tokyo', current_timestamp(), current_timestamp()),
('hoge5_5@gmail.com', 'mail',   11, 'shirou', 'osaka', current_timestamp(), current_timestamp()),
('hoge6@gmail.com', 'female', 42, 'fumiko', 'tokyo', current_timestamp(), current_timestamp());