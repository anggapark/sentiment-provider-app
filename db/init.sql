-- reviewId,userName,userImage,content,score,thumbsUpCount,reviewCreatedVersion,at,replyContent,repliedAt,appVersion,sentiment

CREATE TABLE telkom_db (
    reviewId VARCHAR PRIMARY KEY,
    userName VARCHAR(255),         -- increased from 100
    userImage VARCHAR(1000),       -- increased from 100
    content TEXT,                  -- changed from VARCHAR(500) to TEXT
    score INT,
    thumbsUpCount INT,
    reviewCreatedVersion VARCHAR(50),  -- increased from 10
    at VARCHAR(50),                    -- increased from 20
    replyContent TEXT,                 -- changed from VARCHAR(500) to TEXT
    repliedAt VARCHAR(50),             -- increased from 20
    appVersion VARCHAR(50),            -- increased from 10
    sentiment VARCHAR(20)              -- changed from CHAR(10)
);

CREATE TABLE xl_db (
    reviewId VARCHAR PRIMARY KEY,
    userName VARCHAR(255),
    userImage VARCHAR(1000),
    content TEXT,
    score INT,
    thumbsUpCount INT,
    reviewCreatedVersion VARCHAR(50),
    at VARCHAR(50),
    replyContent TEXT,
    repliedAt VARCHAR(50),
    appVersion VARCHAR(50),
    sentiment VARCHAR(20)
);

CREATE TABLE indosat_db (
    reviewId VARCHAR PRIMARY KEY,
    userName VARCHAR(255),
    userImage VARCHAR(1000),
    content TEXT,
    score INT,
    thumbsUpCount INT,
    reviewCreatedVersion VARCHAR(50),
    at VARCHAR(50),
    replyContent TEXT,
    repliedAt VARCHAR(50),
    appVersion VARCHAR(50),
    sentiment VARCHAR(20)
);

CREATE TABLE smartfren_db (
    reviewId VARCHAR PRIMARY KEY,
    userName VARCHAR(255),
    userImage VARCHAR(1000),
    content TEXT,
    score INT,
    thumbsUpCount INT,
    reviewCreatedVersion VARCHAR(50),
    at VARCHAR(50),
    replyContent TEXT,
    repliedAt VARCHAR(50),
    appVersion VARCHAR(50),
    sentiment VARCHAR(20)
);

\COPY telkom_db(reviewId, userName, userImage, content, score, thumbsUpCount, reviewCreatedVersion, at, replyContent, repliedAt, appVersion, sentiment) FROM '/docker-entrypoint-initdb.d/data/MyTelkomsel-v2.csv' DELIMITER ',' CSV HEADER;

\COPY xl_db(reviewId, userName, userImage, content, score, thumbsUpCount, reviewCreatedVersion, at, replyContent, repliedAt, appVersion, sentiment) FROM '/docker-entrypoint-initdb.d/data/MyXL-v2.csv' DELIMITER ',' CSV HEADER;

\COPY indosat_db(reviewId, userName, userImage, content, score, thumbsUpCount, reviewCreatedVersion, at, replyContent, repliedAt, appVersion, sentiment) FROM '/docker-entrypoint-initdb.d/data/MyIM3-v2.csv' DELIMITER ',' CSV HEADER;

\COPY smartfren_db(reviewId, userName, userImage, content, score, thumbsUpCount, reviewCreatedVersion, at, replyContent, repliedAt, appVersion, sentiment) FROM '/docker-entrypoint-initdb.d/data/MySF-v2.csv' DELIMITER ',' CSV HEADER;

