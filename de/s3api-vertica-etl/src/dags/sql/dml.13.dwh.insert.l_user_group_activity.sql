INSERT INTO GEORGYVREPINYANDEXRU__DWH.l_user_group_activity (hk_l_user_group_activity, hk_user_id, hk_group_id,load_dt,load_src)
select distinct
hash(hk_user_id,hk_group_id),
hu.hk_user_id,
hg.hk_group_id,
now() as load_dt,
's3' as load_src
from GEORGYVREPINYANDEXRU__STAGING.group_log as l
left join GEORGYVREPINYANDEXRU__DWH.h_users as hu on l.user_id = hu.user_id
left join GEORGYVREPINYANDEXRU__DWH.h_groups as hg on l.group_id  = hg.group_id
where hash(hk_user_id,hk_group_id) not in (select hk_l_user_group_activity from GEORGYVREPINYANDEXRU__DWH.l_user_group_activity);
