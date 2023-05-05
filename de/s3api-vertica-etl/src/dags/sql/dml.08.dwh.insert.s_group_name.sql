INSERT INTO  GEORGYVREPINYANDEXRU__DWH.s_group_name(hk_group_id, group_name, load_dt, load_src)
select hg.hk_group_id,
g.group_name,
now() as load_dt,
's3' as load_src
from  GEORGYVREPINYANDEXRU__DWH.h_groups as hg
left join  GEORGYVREPINYANDEXRU__STAGING.groups as g on hg.group_id = g.id;
