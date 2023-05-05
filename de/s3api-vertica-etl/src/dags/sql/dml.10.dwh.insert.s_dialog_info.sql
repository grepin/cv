INSERT INTO  GEORGYVREPINYANDEXRU__DWH.s_dialog_info(hk_message_id, message, message_from, message_to, load_dt, load_src)
select hd.hk_message_id ,
d.message ,
d.message_from ,
d.message_to,
now() as load_dt,
's3' as load_src
from  GEORGYVREPINYANDEXRU__DWH.h_dialogs  as hd
left join  GEORGYVREPINYANDEXRU__STAGING.dialogs as d on hd.message_id  = d.message_id ;
