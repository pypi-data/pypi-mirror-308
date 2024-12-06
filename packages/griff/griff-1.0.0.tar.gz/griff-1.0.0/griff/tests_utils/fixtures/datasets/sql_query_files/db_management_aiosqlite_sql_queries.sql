-- name: create_test_table#
create table user_account
(
    email      VARCHAR  not null
        primary key,
    password   VARCHAR  not null,
    status     VARCHAR  not null,
    token      VARCHAR,
    created_at timestamp with time zone not null,
    updated_at timestamp with time zone not null
);

-- name: drop_test_table#
drop table user_account;

-- name: get_table_by_name^
SELECT name
FROM sqlite_master where name like 'user_account';

-- name: insert_test_data!
INSERT INTO user_account (email, password, status, token, created_at, updated_at)
VALUES ('bertrand.begouin@gmail.com',
        '$pbkdf2-sha256$29000$2BvjXEsJAcB4790bo1QqZQ$lzvYdHZTi78BMht0pbhSW/HYNKyyDHozW.VBOhNABm8',
        '14778763-0928-4444-93e8-a44f756b6399',
        'WAITING_EMAIL_CONFIRM',
        '2023-04-08 11:11:11.111111',
        '2023-04-08 11:11:11.111111');

-- name: insert_parametrized_test_data!
INSERT INTO user_account (email, password, status, token, created_at, updated_at)
VALUES (:email, :password, :status, :token, :created_at, :updated_at);

-- name: select_all^
SELECT email as email,
       password as password,
       status as status,
       token as token,
       strftime('%Y-%m-%d %H:%M:%S', created_at) as created_at,
       strftime('%Y-%m-%d %H:%M:%S', updated_at) as updated_at
FROM user_account;