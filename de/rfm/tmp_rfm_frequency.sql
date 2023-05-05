delete from analysis.tmp_rfm_frequency
;

insert into analysis.tmp_rfm_frequency
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
		count(o.order_id) "order_count"
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
	ntile(5) over (order by order_count asc nulls first) "frequency"
from ps
;


select 
	frequency,
	count(frequency)
from 
	analysis.tmp_rfm_frequency
group by
	frequency
order by 
	frequency
;





