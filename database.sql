DROP TABLE IF EXISTS urls CASCADE;

CREATE TABLE urls (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY, 
    name varchar(255) UNIQUE, 
    created_at timestamp
    );

DROP TABLE IF EXISTS url_checks;

CREATE TABLE url_checks (
    id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    url_id bigint REFERENCES urls (id),
    h1 varchar(255),
    title varchar(255),
    description varchar(255),
    status_code smallint,
    created_at timestamp
);
