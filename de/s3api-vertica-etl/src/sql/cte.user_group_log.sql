with user_group_log as (
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
	hk_group_id,
	cnt_added_users
from user_group_log
order by cnt_added_users
limit 10
