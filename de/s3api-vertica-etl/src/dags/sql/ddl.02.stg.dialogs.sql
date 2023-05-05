create table if not exists GEORGYVREPINYANDEXRU__STAGING.dialogs
(
	message_id int primary key,
	message_ts timestamp(6),
	message_from int references GEORGYVREPINYANDEXRU__STAGING.users(id),
	message_to int references GEORGYVREPINYANDEXRU__STAGING.users(id),
	message varchar(1000),
	message_group int references GEORGYVREPINYANDEXRU__STAGING.groups(id)
)
order by message_id
SEGMENTED BY hash(message_id) all nodes
PARTITION BY message_ts::date
GROUP BY calendar_hierarchy_day(message_ts::date, 3, 2)
;
