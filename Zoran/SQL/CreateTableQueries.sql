Select * From articles
Select * From company
Select * From designs
Select * From limited_edition
Select * From producttype
Select * From releaseyear
Select * From sizes


CREATE TABLE company (
    companynr SERIAL PRIMARY KEY NOT NULL,
    companyname TEXT,
    adress TEXT,
    postalcode VARCHAR,
    location TEXT,
    country VARCHAR
);

CREATE TABLE articles (
    articlenr SERIAL PRIMARY KEY NOT NULL,
    producttype TEXT,
    design TEXT,
    companyname TEXT,
    size TEXT,
    quantity INTEGER DEFAULT 0
);

CREATE TABLE Designs (
    designnr SERIAL PRIMARY KEY NOT NULL,
    designname TEXT
);

CREATE TABLE producttype (
    typenr SERIAL PRIMARY KEY NOT NULL,
    typename TEXT
);

CREATE TABLE Releaseyear (
    releaseyear INT
);

CREATE TABLE Sizes (
    Sizenr SERIAL PRIMARY KEY NOT NULL,
    size TEXT
);

CREATE TABLE Limited_edition (
    lenr SERIAL PRIMARY KEY NOT NULL,
    le TEXT
);
