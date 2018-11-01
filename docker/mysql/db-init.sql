create database abbey;

use abbey;

create table users(
    id int primary key auto_increment,
    username varchar(32),
    passwd varchar(32),
    email varchar(64),
    realname varchar(32),
    index (username));

create table tasks(
    id varchar(16) primary key,
    title varchar(64));

create table blobs(
    id varchar(32) primary key,
    val blob);

create table userblobs(
    id varchar(32) primary key,
    val blob);

create table usertask(
    userid int,
    taskid varchar(16),
    solved int default 0,
    ts int,
    index (userid), index(taskid));

create table srvsession(
    userid int primary key,
    val text);

create table actionlog(
    ts int,
    userid int,
    action varchar(8),
    txt varchar(32),
    index (userid), index(ts));

create table taskstats (taskid varchar(16) primary key, cat varchar(16), solved int, cost float);

create table userstats (
    userid int,
    cat varchar(16),
    cnt int,
    cost float,
    primary key (userid, cat),
    index (userid), index(cat));

create view taskcounts as
    select id as taskid, ifnull(cnt, 0) + 1 as cnt, left(id, instr(id, '-') - 1) as cat
    from tasks left join
        (select taskid, count(1) as cnt from usertask where solved > 0 group by taskid) sol
    on id = sol.taskid where id not like '!%';

create view taskstats_v as
    select taskid, cat, cnt, 1+log10(mc/cnt)*4 as cost
    from taskcounts tc join (select cat, max(cnt) as mc from taskcounts group by cat) m using (cat);

create view userstats_v as
    select userid, cat, count(1) as cnt, sum(cost) as res
    from usertask tu join taskstats ts on tu.taskid = ts.taskid where tu.solved=1 group by userid, cat;

insert into tasks values ('!prg', 'Programming Problems');
insert into tasks values ('!qz', 'Programming Quizes');

insert into tasks values ('prg-1', 'Sum of Two');
insert into blobs values ('t.prg-1.en', 'You are given two **integer** values and need to tell their sum...');
insert into blobs values ('t.prg-1.chk', x'696d706f72742072616e646f6d0a0a61203d2072616e646f6d2e72616e64696e7428333030302c203136303030290a62203d2072616e646f6d2e72616e64696e7428333030302c203136303030290a0a696e7075745f64617461203d202225732025732220252028612c2062290a65787065637465645f616e73776572203d207374722861202b2062290a0a');

insert into tasks values ('prg-2', 'Fahrenheit to Celsius');
insert into blobs values ('t.prg-2.en', 'Now we want to process list of integers, pretending they are temperature values in `Fahrenheit` and converting them to `Celsius` degrees.');

insert into tasks values ('prg-3', 'Vowel count');
insert into blobs values ('t.prg-3.en', 'Given several strings of text please tell how many vowels contain each of them.');

insert into tasks values ('qz-1', 'Search Complexity');
insert into blobs values ('t.qz-1.en', x'506c656173652c20616e73776572206f6e207468652074696d6520636f6d706c6578697479206f6620616c676f726974686d730a');
insert into blobs values ('t.qz-1.chk', x'636865636b5f74797065203d20277175697a270a0a696e7075745f64617461203d205b0a202020207b0a20202020202020202771273a2027536561726368696e6720666f7220656c656d656e7420696e2074686520756e736f72746564206172726179206973272c0a20202020202020202774797065273a202773696e676c65272c0a2020202020202020276974656d73273a205b274f286c6f67284e2929272c20274f283129272c20274f284e29272c20274f284e5e3229272c20274f284e2a6c6f67284e2929275d0a202020207d2c0a202020207b0a20202020202020202771273a2027536561726368696e6720666f7220656c656d656e7420696e2074686520736f72746564206172726179206973272c0a20202020202020202774797065273a202773696e676c65272c0a2020202020202020276974656d73273a205b274f286c6f67284e2929272c20274f283129272c20274f284e29272c20274f284e5e3229272c20274f284e2a6c6f67284e2929275d0a202020207d2c0a202020207b0a20202020202020202771273a20274665746368696e6720656c656d656e742066726f6d20686173687461626c652028486173684d61702c2064696374282929206973272c0a20202020202020202774797065273a202773696e676c65272c0a2020202020202020276974656d73273a205b274f286c6f67284e2929272c20274f283129272c20274f284e29272c20274f284e5e3229272c20274f284e2a6c6f67284e2929275d0a202020207d0a5d0a0a65787065637465645f616e73776572203d20223032203130203231220a');

insert into users (username, passwd, email) values ('testuser', 'UjcJRRppx+E2tR/YPFd7k1Ivy34mQ2oK', 'test@user.mail');

insert into blobs values ('wk.help.en', x'232047656e6572616c2048656c700a0a5468697320697320612068656c7020706167650a');

