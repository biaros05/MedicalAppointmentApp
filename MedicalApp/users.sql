create table medical_access_level(
    user_type varchar2(20) PRIMARY KEY,
    CONSTRAINT check_user_type
    CHECK (user_type IN('BLOCKED','PATIENT', 'STAFF', 'ADMIN_USER', 'ADMIN'))
);

CREATE TABLE medical_users (
    id          INTEGER
        GENERATED BY DEFAULT ON NULL AS IDENTITY
    PRIMARY KEY,
    email       VARCHAR2(100) NOT NULL UNIQUE,
    password    VARCHAR2(162) NOT NULL,
    first_name  VARCHAR2(1000) NOT NULL,
    last_name   VARCHAR2(1000) NOT NULL,
    avatar_path VARCHAR2(2000),
    user_type   VARCHAR2(20) REFERENCES medical_access_level(user_type)
);


CREATE TABLE medical_api_tokens(
user_id integer not null,
token VARCHAR2(162) not null,
CONSTRAINT user_fk FOREIGN KEY (user_id) REFERENCES medical_users(id)
);

/*
ALTER TABLE medical_users
    ADD UNIQUE (EMAIL);
*/