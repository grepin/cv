create table if not exists GEORGYVREPINYANDEXRU__STAGING.users
(
	id int primary key,
	chat_name varchar(200),
	registration_dt timestamp(6),
	country varchar(200),
	age int
)
order by id
SEGMENTED BY hash(id) all nodes
;
