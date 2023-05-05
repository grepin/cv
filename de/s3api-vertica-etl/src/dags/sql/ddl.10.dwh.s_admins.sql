create table if not exists GEORGYVREPINYANDEXRU__DWH.s_admins
(
    hk_admin_id bigint not null CONSTRAINT fk_s_admins_l_admins REFERENCES  GEORGYVREPINYANDEXRU__DWH.l_admins (hk_l_admin_id),
    is_admin boolean,
    admin_from datetime,
    load_dt datetime,
    load_src varchar(20)
)
order by load_dt
SEGMENTED BY hk_admin_id all nodes
PARTITION BY load_dt::date
GROUP BY calendar_hierarchy_day(load_dt::date, 3, 2);
