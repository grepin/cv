delete from analysis.tmp_rfm_monetary_value
;

insert into analysis.tmp_rfm_monetary_value
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
		sum(cost) "orders_sum"
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
	ntile(5) over (order by orders_sum asc nulls first) "monetary_value"
from ps
;

select 
	monetary_value,
	count(monetary_value)
from 
	analysis.tmp_rfm_monetary_value
group by
	monetary_value
order by 
	monetary_value
;





