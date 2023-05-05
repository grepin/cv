INSERT INTO GEORGYVREPINYANDEXRU__DWH.l_groups_dialogs  (hk_l_groups_dialogs, hk_message_id, hk_group_id, load_dt,load_src)
select
hash(hk_message_id, hk_group_id),
hd.hk_message_id,
hg.hk_group_id,
now() as load_dt,
's3' as load_src
from GEORGYVREPINYANDEXRU__STAGING.dialogs as d
left join GEORGYVREPINYANDEXRU__DWH.h_dialogs as hd on d.message_id = hd.message_id
left join GEORGYVREPINYANDEXRU__DWH.h_groups as hg on d.message_group = hg.group_id
where hash(hk_message_id, hk_group_id) not in (select hk_l_groups_dialogs from GEORGYVREPINYANDEXRU__DWH.l_groups_dialogs) and hg.group_id is not null;
