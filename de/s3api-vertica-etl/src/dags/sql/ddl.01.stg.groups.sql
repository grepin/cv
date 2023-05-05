create table if not exists GEORGYVREPINYANDEXRU__STAGING.groups
(
	id int primary key,
	admin_id int references GEORGYVREPINYANDEXRU__STAGING.users(id),
	group_name varchar(100),
	registration_dt timestamp(6),
	is_private varchar(100)
)
order by id, admin_id
SEGMENTED BY hash(id) all nodes
PARTITION BY registration_dt::date
GROUP BY calendar_hierarchy_day(registration_dt::date, 3, 2)
