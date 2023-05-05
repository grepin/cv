create table if not exits GEORGYVREPINYANDEXRU__DWH.s_auth_history
(
	hk_l_user_group_activity bigint,
	user_id_from bigint,
	event varchar(8),
	event_dt timestamp(6),
	load_dt datetime,
	load_src varchar(20)
)
order by load_dt
SEGMENTED BY hk_l_user_group_activity all nodes
PARTITION BY load_dt::date
GROUP BY calendar_hierarchy_day(load_dt::date, 3, 2);