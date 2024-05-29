create table store_shippingaddress
(
    id          integer  not null
        primary key autoincrement,
    address     varchar(200),
    city        varchar(200),
    state       varchar(200),
    zipcode     varchar(200),
    date_added  datetime not null,
    customer_id bigint
        references store_customer
            deferrable initially deferred,
    order_id    bigint
        references store_order
            deferrable initially deferred
);

create index store_shippingaddress_customer_id_66e362a6
    on store_shippingaddress (customer_id);

create index store_shippingaddress_order_id_e6decfbb
    on store_shippingaddress (order_id);

