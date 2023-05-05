with user_group_messages as (
	select
    	hk_group_id,
		count(1) "cnt_users_in_group_with_messages"
    from (
		select
			distinct
			    hk_group_id,
		    	hu.hk_user_id
		from
		    GEORGYVREPINYANDEXRU__DWH.l_groups_dialogs lgd
		left join
			GEORGYVREPINYANDEXRU__DWH.l_user_message lum
			on lgd.hk_message_id = lum.hk_message_id
		left JOIN
			GEORGYVREPINYANDEXRU__DWH.h_users hu
			on lum.hk_user_id = hu.hk_user_id
    ) u2m
    group by hk_group_id
), user_group_log as (
	select
	    hk_group_id,
		count(1) "cnt_added_users"
	from (
		select
			distinct
				luga.hk_group_id,
				luga.hk_user_id
		from
			(select hk_group_id from GEORGYVREPINYANDEXRU__DWH.h_groups order by registration_dt limit 10) hg
		left join
			GEORGYVREPINYANDEXRU__DWH.l_user_group_activity luga
			on luga.hk_group_id = hg.hk_group_id
		left join
			GEORGYVREPINYANDEXRU__DWH.s_auth_history sah
				on 1 = 1
					and luga.hk_l_user_group_activity = sah.hk_l_user_group_activity
					and sah.event = 'add'
	) g2au
	group by hk_group_id
)
select  
    ugl.hk_group_id,
    cnt_added_users,
    cnt_users_in_group_with_messages,
    (ugm.cnt_users_in_group_with_messages / ugl.cnt_added_users) "group_conversion"
from 
    user_group_log as ugl
left join 
    user_group_messages as ugm on ugl.hk_group_id = ugm.hk_group_id
order by ugm.cnt_users_in_group_with_messages / ugl.cnt_added_users desc 
