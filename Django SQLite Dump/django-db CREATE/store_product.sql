create table store_product
(
    id      integer      not null
        primary key autoincrement,
    name    varchar(200) not null,
    price   real         not null,
    digital bool,
    image   varchar(100)
);

