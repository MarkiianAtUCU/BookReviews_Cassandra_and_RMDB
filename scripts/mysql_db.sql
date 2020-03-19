create database bookstore;
create user '<user>'@'%' identified by '<password>';
GRANT ALL PRIVILEGES ON bookstore.* TO '<user>'@'%';
flush PRIVILEGES;

USE bookstore;

CREATE TABLE category (
	id int auto_increment primary key,
	name tinytext
);

CREATE TABLE marketplace (
	id int auto_increment primary key,
	name char(2)
);

CREATE TABLE product (
	id char(10) primary key,
	parent text,
	title text,
	category_id int,
    foreign key (category_id) references category(id)
);

CREATE TABLE review (
	id char(13) primary key,
	product_id char(10),
	marketplace_id int,
	customer_id int,
	star_rating tinyint,
	helpful_votes int,
	total_votes int,
	vine boolean,
	verified_purchase boolean,
	headline text,
	body mediumtext,
	date date,
    foreign key (product_id) references product(id),
    foreign key (marketplace_id) references marketplace(id)
	);