create table if not exists GEORGYVREPINYANDEXRU__DWH.l_groups_dialogs
(
	hk_l_groups_dialogs bigint primary key,
	hk_message_id  bigint not null CONSTRAINT fk_l_groups_dialogs_message REFERENCES GEORGYVREPINYANDEXRU__DWH.h_dialogs (hk_message_id),
	hk_group_id bigint not null CONSTRAINT fk_l_groups_dialogs_group REFERENCES GEORGYVREPINYANDEXRU__DWH.h_groups (hk_group_id),
	load_dt datetime,
	load_src varchar(20)
)
order by load_dt
SEGMENTED BY hk_l_groups_dialogs all nodes
PARTITION BY load_dt::date
GROUP BY calendar_hierarchy_day(load_dt::date, 3, 2);
