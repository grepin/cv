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
)
select
    hk_group_id,
    cnt_users_in_group_with_messages
from user_group_messages
order by cnt_users_in_group_with_messages
limit 10