create database abbey;

use abbey;

create table users(id int primary key auto_increment, username varchar(32), passwd varchar(32), email varchar(64), realname varchar(32));

create table tasks(id varchar(16) primary key, title varchar(64));

create table blobs(id varchar(32) primary key, val blob);

insert into tasks values ('prg-1', 'Sum of Two');
insert into blobs values('t.prg-1.en', 'You are given two **integer** values and need to tell their sum...');
insert into tasks values ('prg-2', 'Fahrenheit to Celsius');
insert into blobs values('t.prg-2.en', 'Now we want to process list of integers, pretending they are temperature values in `Fahrenheit` and converting them to `Celsius` degrees.');
insert into tasks values ('prg-3', 'Vowel count');
insert into blobs values('t.prg-3.en', 'Given several strings of text please tell how many vowels contain each of them.');

