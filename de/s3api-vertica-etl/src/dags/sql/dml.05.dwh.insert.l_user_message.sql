INSERT INTO GEORGYVREPINYANDEXRU__DWH.l_user_message (hk_l_user_message, hk_user_id, hk_message_id,load_dt,load_src)
select
hash(hk_user_id,hk_message_id),
hu.hk_user_id,
hd.hk_message_id,
now() as load_dt,
's3' as load_src
from GEORGYVREPINYANDEXRU__STAGING.dialogs as d
left join GEORGYVREPINYANDEXRU__DWH.h_users as hu on d.message_from = hu.user_id
left join GEORGYVREPINYANDEXRU__DWH.h_dialogs as hd on d.message_id  = hd.message_id
where hash(hk_user_id,hk_message_id) not in (select hk_l_user_message from GEORGYVREPINYANDEXRU__DWH.l_user_message);
