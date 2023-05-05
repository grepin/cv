INSERT INTO GEORGYVREPINYANDEXRU__DWH.h_users(hk_user_id, user_id,registration_dt,load_dt,load_src)
select
       hash(id) as  hk_user_id,
       id as user_id,
       registration_dt,
       now() as load_dt,
       's3' as load_src
       from GEORGYVREPINYANDEXRU__STAGING.users
where hash(id) not in (select hk_user_id from GEORGYVREPINYANDEXRU__DWH.h_users);
