drop view if exists analysis.orders;

create view analysis.orders as 
select 
	o.order_id,
	o.order_ts,
	o.user_id,
	o.bonus_payment,
	o.payment,
	o.cost,
	o.bonus_grant,
	osl.status_id "status"
from 
	production.orders o 
inner join
	production.orderstatuslog osl
		on 1 = 1
		and o.order_id = osl.order_id 
		and o.order_ts = osl.dttm 
where osl.dttm >= '2022-01-01'
