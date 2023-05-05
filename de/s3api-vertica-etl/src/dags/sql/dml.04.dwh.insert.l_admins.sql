INSERT INTO GEORGYVREPINYANDEXRU__DWH.l_admins(hk_l_admin_id, hk_group_id,hk_user_id,load_dt,load_src)
select
hash(hg.hk_group_id,hu.hk_user_id),
hg.hk_group_id,
hu.hk_user_id,
now() as load_dt,
's3' as load_src
from GEORGYVREPINYANDEXRU__STAGING.groups as g
left join GEORGYVREPINYANDEXRU__DWH.h_users as hu on g.admin_id = hu.user_id
left join GEORGYVREPINYANDEXRU__DWH.h_groups as hg on g.id = hg.group_id
where hash(hg.hk_group_id,hu.hk_user_id) not in (select hk_l_admin_id from GEORGYVREPINYANDEXRU__DWH.l_admins);
