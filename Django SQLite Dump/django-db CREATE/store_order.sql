create table store_order
(
    id             integer  not null
        primary key autoincrement,
    date_ordered   datetime not null,
    complete       bool     not null,
    transaction_id varchar(100),
    customer_id    bigint
        references store_customer
            deferrable initially deferred
);

create index store_order_customer_id_13d6d43e
    on store_order (customer_id);

