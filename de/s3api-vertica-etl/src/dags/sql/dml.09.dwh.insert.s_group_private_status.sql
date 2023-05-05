INSERT INTO  GEORGYVREPINYANDEXRU__DWH.s_group_private_status(hk_group_id, is_private, load_dt, load_src)
select hg.hk_group_id,
g.is_private = '1',
now() as load_dt,
's3' as load_src
from  GEORGYVREPINYANDEXRU__DWH.h_groups as hg
left join  GEORGYVREPINYANDEXRU__STaGING.groups as g on hg.group_id = g.id;
