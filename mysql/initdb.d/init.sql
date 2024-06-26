CREATE TABLE `event` (
    event_id        VARCHAR(100) UNIQUE NOT NULL,
    event_name      VARCHAR(100)        NOT NULL,
    organization_id VARCHAR(100)        NOT NULL DEFAULT 'unknown',
    pswd            VARCHAR(100)        NOT NULL,
    ticket_num      INT                 NOT NULL,
    event_date      DATETIME(6)         NOT NULL,
    public_date     DATETIME(6)         NOT NULL,
    version         INT                 NOT NULL DEFAULT 1,
    created_at      DATETIME(6)         NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at      DATETIME(6)         NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    deleted         BOOLEAN             NOT NULL DEFAULT FALSE,
    PRIMARY KEY (event_id)
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
    version         INT          NOT NULL DEFAULT 1,
    created_at      DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    updated_at      DATETIME(6)  NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    deleted         BOOLEAN      NOT NULL DEFAULT FALSE,
    PRIMARY KEY (ticket_id, event_id),
    FOREIGN KEY (event_id) REFERENCES event(event_id)
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


INSERT INTO `event` (event_id, event_name, pswd, ticket_num, event_date, public_date)
VALUES
('test0', '終了イベント', MD5('pass'), 20, '2020-9-20', '2020-9-20'),
('test1', '表示テスト', MD5('pass'), 20, '2024-10-20', '2020-9-20'),
('test2', '登録日前', MD5('pass'), 12, '2024-10-20', '2024-10-20'),
('test3', 'チケット枚数足りない', MD5('pass'), 1, '2024-10-20', '2020-10-20');

INSERT INTO `ticket` (ticket_id, event_id, name, phone_number, email, family_id, comment, memo, deleted)
VALUES
(1, 'test1', 'name1', '08012345678', 'test@mail.com', 'family1', '', '', FALSE),
(2, 'test1', 'name2', '08012345678', 'test@mail.com', 'family1', '', '', FALSE),
(3, 'test1', 'name3', '08012345678', 'test@mail.com', 'family1', '', '', TRUE),
(4, 'test1', 'name4', '08012345678', 'test@mail.com', 'family2', '', '', FALSE),
(5, 'test1', 'name5', '08012345678', 'test@mail.com', 'family3', '', '', FALSE),
(1, 'test3', 'name1', '08012345678', 'test@mail.com', 'family1', '', '', FALSE);


INSERT INTO `personal_info` (mail_address, sex, age, name, prefecture, createdAt, updatedAt)
VALUES
('hoge1_1@gmail.com', 'male',   18, 'ichirou1' , 'tokyo', current_timestamp(), current_timestamp()),
('hoge2@gmail.com', 'male',   23, 'zirou2', 'osaka', current_timestamp(), current_timestamp()),
('hoge3_3@gmail.com', 'male',   31, 'saburou', 'tokyo', current_timestamp(), current_timestamp()),
('hoge4@gmail.com', 'female', 29, 'itiko', 'tokyo', current_timestamp(), current_timestamp()),
('hoge5_5@gmail.com', 'mail',   11, 'shirou', 'osaka', current_timestamp(), current_timestamp()),
('hoge6@gmail.com', 'female', 42, 'fumiko', 'tokyo', current_timestamp(), current_timestamp());