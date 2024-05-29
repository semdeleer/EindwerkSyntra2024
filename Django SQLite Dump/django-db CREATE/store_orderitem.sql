create table store_orderitem
(
    id         integer  not null
        primary key autoincrement,
    quantity   integer,
    date_added datetime not null,
    order_id   bigint
        references store_order
            deferrable initially deferred,
    product_id bigint
        references store_product
            deferrable initially deferred
);

create index store_orderitem_order_id_acf8722d
    on store_orderitem (order_id);

create index store_orderitem_product_id_f2b098d4
    on store_orderitem (product_id);

