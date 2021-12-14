create table "user"
	(user_id		serial,
	 first_name		varchar(20) not null,
	 last_name		varchar(20) not null,
	 email_address		varchar(60) unique not null,
	 password 		text not null,
	 billing_address		varchar(100) not null,
	 shipping_address		varchar(100) not null,
	 primary key (user_id)
	);
create table owner
	(owner_id		serial,
	 email_address		varchar(60) unique not null,
	 password		text not null,
	 primary key (owner_id)
	);

create table publisher
	(publisher_id		serial,
	 name		varchar(40) unique not null,
	 email_address		varchar(60) unique not null,
	 institution_no		varchar(3) not null,
	 transit_no		varchar(5) not null,
	 account_no		varchar(7) not null, 
	 primary key (publisher_id)
	);

create table book
	(ISBN		varchar(13),
	 publisher_id		int not null,
	 title		varchar(60) not null,
	 genre		varchar(20) not null,
	 stock_quantity		int not null
	 	check (stock_quantity >= 0),
	 price		numeric(8,2) not null,
	 num_pages		int not null
	 	check (num_pages > 0),
	 publisher_percentage		double precision default 40,
	 primary key(ISBN),
	 foreign key(publisher_id) references publisher
	);

create table author
	(ISBN		varchar(13),
	 first_name		varchar(20),
	 last_name		varchar(20),
	 primary key (ISBN, first_name, last_name),
	 foreign key (ISBN) references book
	 	on delete cascade
	);

create table "order"
	(order_number		serial,
	 user_id		int not null,
	 order_date		Date not null default current_date,
	 total		numeric(8,2) not null,
	 shipping_address		varchar(100) not null,
	 billing_address		varchar(100) not null,
	 order_status		varchar(15) default 'At warehouse',
	 primary key(order_number),
	 foreign key(user_id) references "user" on delete cascade
	);

create table contains
	(order_number		int not null,
	 ISBN		varchar(13),
	 sold_quantity		int not null
	 	check (sold_quantity > 0),	
	 primary key (order_number, ISBN),
	 foreign key (ISBN) references book
	 	on delete set null,
	 foreign key (order_number) references "order" on delete cascade
	);


create table user_phone
	(user_id		int not null,
	 phone_number		varchar(11) not null,
	 foreign key(user_id) references "user" on delete cascade,
	 primary key(user_id, phone_number)
	);

create table publisher_phone
	(publisher_id		int not null,
	 phone_number		varchar(11) not null,
	 foreign key(publisher_id) references publisher on delete cascade,
	 primary key(publisher_id, phone_number)
	);

create or replace view sales_per_genre as
select genre, sum(price*sold_quantity) as sales
from ("contains" join "order" using (order_number)) join book using(ISBN)
group by genre;

create or replace view sales_per_author as
select first_name, last_name, sum(price*sold_quantity)  as sales
from ("contains" join "order" using (order_number)) join author using(ISBN) join book using(ISBN)
group by first_name, last_name;

create or replace view sales_vs_expenditure as
select ISBN, title, sum(price*(sold_quantity+stock_quantity)) as expenditure, sum(price*sold_quantity) as sales
from book join contains using(ISBN)
group by title, ISBN;

create or replace view publisher_revenue as
select name, title, sum(cast(publisher_percentage/100 as numeric(8,2))*sold_quantity*price) as revenue
from (publisher join book using (publisher_id)) join contains using (ISBN)
group by name, title


alter sequence user_user_id_seq restart with 1 increment by 1;
alter sequence owner_owner_id_seq restart with 1 increment by 1;
alter sequence order_order_number_seq restart with 1 increment by 1;
alter sequence publisher_publisher_id_seq restart with 1 increment by 1;