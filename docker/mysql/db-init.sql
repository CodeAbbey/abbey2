create database abbey;

use abbey;

create table users(
    id int primary key auto_increment,
    username varchar(32),
    passwd varchar(32),
    email varchar(64),
    realname varchar(32),
    index (username));

create table tasks(id varchar(16) primary key, title varchar(64));

create table blobs(id varchar(32) primary key, val blob);

create table usertask(
    userid int(32),
    taskid varchar(16),
    solved int default 0,
    ts timestamp default current_timestamp,
    index (userid), index(taskid));

insert into tasks values ('prg-1', 'Sum of Two');
insert into blobs values('t.prg-1.en', 'You are given two **integer** values and need to tell their sum...');
insert into blobs values('t.prg-1.chk', x'696d706f72742072616e646f6d0a0a61203d2072616e646f6d2e72616e64696e7428333030302c203136303030290a62203d2072616e646f6d2e72616e64696e7428333030302c203136303030290a0a696e7075745f64617461203d202225732025732220252028612c2062290a65787065637465645f616e73776572203d207374722861202b2062290a0a');
insert into tasks values ('prg-2', 'Fahrenheit to Celsius');
insert into blobs values('t.prg-2.en', 'Now we want to process list of integers, pretending they are temperature values in `Fahrenheit` and converting them to `Celsius` degrees.');
insert into tasks values ('prg-3', 'Vowel count');
insert into blobs values('t.prg-3.en', 'Given several strings of text please tell how many vowels contain each of them.');

