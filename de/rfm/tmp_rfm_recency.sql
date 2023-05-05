delete from analysis.tmp_rfm_recency
;

insert into analysis.tmp_rfm_recency
with closed_orders as (
	select 
		* 
	from 
		analysis.orders o
	left join
		analysis.orderstatuses os
			on 1 = 1 
			and o.status = os.id 
	where 
		os.key = 'Closed'
), ps as (
	select 
		u.id,
		max(order_ts) "last_order_date"
	from 
		analysis.users u
	left join
		closed_orders o 
			on 1 = 1
			and o.user_id = u.id
	group by 
		u.id 
) select 
	id,
	ntile(5) over (order by last_order_date asc nulls first) "recency"
from ps
;

select 
	recency,
	count(recency)
from 
	analysis.tmp_rfm_recency
group by
	recency
order by 
	recency
;





