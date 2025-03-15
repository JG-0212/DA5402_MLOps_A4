CREATE TABLE IF NOT EXISTS news_data(
    Title VARCHAR(512) NOT NULL,
    Pub_timestamp TIMESTAMP,
    Weblink VARCHAR(255) NOT NULL,
    Picture BYTEA,
    Tags VARCHAR(255),
    Summary VARCHAR(512),
    PRIMARY KEY (Title, Pub_timestamp)
);