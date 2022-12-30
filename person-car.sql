create table car (
	car_uid UUID NOT NULL PRIMARY KEY,
	make VARCHAR(100) NOT NULL,
	model VARCHAR(100) NOT NULL,
	price NUMERIC(19, 2) NOT NULL
);

create table person (
	person_uid UUID NOT NULL PRIMARY KEY,
	first_name VARCHAR(50)	NOT NULL,
	last_name VARCHAR(50)	NOT NULL,
    gender VARCHAR(15) NOT NULL,
	email VARCHAR(100),
	date_of_birth DATE	NOT NULL,
	country_of_birth VARCHAR(50) NOT NULL,
    car_uid UUID REFERENCES car (car_uid),
    UNIQUE(car_uid),
	UNIQUE(email)
);

insert into person (person_uid, first_name, last_name, email, gender, date_of_birth, country_of_birth) values (uuid_generate_v4(), 'Ethe', 'Ardern', 'eardern0@hibu.com', 'Male', '2022-06-18', 'Philippines');
insert into person (person_uid, first_name, last_name, email, gender, date_of_birth, country_of_birth) values (uuid_generate_v4(), 'Ignacio', 'Charleston', 'icharleston1@ameblo.jp', 'Male', '2022-08-19', 'Egypt');
insert into person (person_uid, first_name, last_name, email, gender, date_of_birth, country_of_birth) values (uuid_generate_v4(), 'Dolph', 'Miko', 'dmiko2@youku.com', 'Male', '2021-12-30', 'China');

insert into car (car_uid, make, model, price) values (uuid_generate_v4(), 'Ford', 'Festiva', '71127.50');
insert into car (car_uid, make, model, price) values (uuid_generate_v4(), 'Nissan', 'Altima', '48611.06');