create table if not exists GEORGYVREPINYANDEXRU__DWH.s_dialog_info
(
    hk_message_id bigint not null CONSTRAINT fk_s_dialog_info_h_dialog REFERENCES  GEORGYVREPINYANDEXRU__DWH.h_dialogs (hk_message_id),
    message varchar(1000),
    message_from int ,
    message_to int ,
    load_dt datetime,
    load_src varchar(20)
)
order by load_dt
SEGMENTED BY hk_message_id all nodes
PARTITION BY load_dt::date
GROUP BY calendar_hierarchy_day(load_dt::date, 3, 2);
