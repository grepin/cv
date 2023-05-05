create table if not exists GEORGYVREPINYANDEXRU__DWH.l_admins
(
	hk_l_admin_id bigint primary key,
	hk_user_id  bigint not null CONSTRAINT fk_l_admins_user REFERENCES GEORGYVREPINYANDEXRU__DWH.h_users (hk_user_id),
	hk_group_id bigint not null CONSTRAINT fk_l_admins_group REFERENCES GEORGYVREPINYANDEXRU__DWH.h_groups (hk_group_id),
	load_dt datetime,
	load_src varchar(20)
)
order by load_dt
SEGMENTED BY hk_l_admin_id all nodes
PARTITION BY load_dt::date
GROUP BY calendar_hierarchy_day(load_dt::date, 3, 2);
