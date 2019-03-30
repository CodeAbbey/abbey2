create database abbey;
create user 'webdbuser'@'localhost' identified by 'w3bp@ssw0rd';
grant select,insert,update,delete on abbey.* to 'webdbuser'@'localhost';

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
    index (userid), index(cat), index(cnt), index(cost));

create table usertop (userid int, cat varchar(16), cnt int, cost float);

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
