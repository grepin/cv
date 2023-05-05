create table if not exists GEORGYVREPINYANDEXRU__STAGING.group_log
(
	group_id int references GEORGYVREPINYANDEXRU__STAGING.groups(id),
	user_id int references GEORGYVREPINYANDEXRU__STAGING.users(id),
	user_id_from int references GEORGYVREPINYANDEXRU__STAGING.users(id),
	event varchar(8),
	datetime timestamp(6)
)
order by group_id, user_id
SEGMENTED BY hash(group_id) all nodes
PARTITION BY datetime::date
GROUP BY calendar_hierarchy_day(datetime::date, 3, 2)
