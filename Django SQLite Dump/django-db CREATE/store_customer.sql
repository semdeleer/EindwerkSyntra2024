create table store_customer
(
    id      integer      not null
        primary key autoincrement,
    name    varchar(200),
    email   varchar(200) not null,
    user_id integer
        unique
        references auth_user
            deferrable initially deferred
);

