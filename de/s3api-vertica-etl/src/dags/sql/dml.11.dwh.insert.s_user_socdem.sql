INSERT INTO  GEORGYVREPINYANDEXRU__DWH.s_user_socdem(hk_user_id, country, age, load_dt, load_src)
select hu.hk_user_id ,
u.country ,
u.age,
now() as load_dt,
's3' as load_src
from  GEORGYVREPINYANDEXRU__DWH.h_users  as hu
left join  GEORGYVREPINYANDEXRU__STaGING.users  as u on hu.user_id  = u.id  ;
