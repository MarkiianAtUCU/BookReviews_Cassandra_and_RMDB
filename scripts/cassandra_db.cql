CREATE KEYSPACE bookstore;
WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 2};

USE bookstore;

CREATE TABLE reviews_by_fraction_of_five  (
    fake_partition int,
    fraction_of_five float,
     product_id text,
    product_category text,
    product_title text,
    PRIMARY KEY ((fake_partition), fraction_of_five, product_id)
) WITH CLUSTERING ORDER BY (fraction_of_five DESC);

CREATE TABLE reviews_by_customer  (
    marketplace text,
    customer_id int,
    review_id text,
    product_id text,
    product_parent text,
    product_title text,
    product_category text,
    star_rating tinyint,
    helpful_votes int,
    total_votes int,
    vine boolean,
    verified_purchase boolean,
    review_headline text,
    review_body	text,
    review_date date,
    PRIMARY KEY ((customer_id), review_id)
);

CREATE TABLE reviews_by_product  (
    marketplace text,
    customer_id int,
    review_id text,
    product_id text,
    product_parent text,
    product_title text,
    product_category text,
    star_rating tinyint,
    helpful_votes int,
    total_votes int,
    vine boolean,
    verified_purchase boolean,
    review_headline text,
    review_body	text,
    review_date date,
    PRIMARY KEY ((product_id), star_rating, review_id)
);

CREATE TABLE reviews_by_date_star  (
    marketplace text,
    product_parent text,
    review_date date,
    verified_purchase boolean,
    star_rating tinyint,
    review_id text,
    customer_id int,
    product_category text,
    product_id text,
    product_title text,

    PRIMARY KEY ((review_date), verified_purchase, star_rating, review_id)
);