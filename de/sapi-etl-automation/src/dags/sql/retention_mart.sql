

create table if not exists mart.f_customer_retention (
	id serial,
	new_customers_count integer,
	returning_customers_count integer,
	refunded_customer_count integer,
	period_name varchar(8),
	period_id integer,
	item_id integer references mart.d_item (item_id), 
	new_customers_revenue numeric (14,2),
	returning_customers_revenue numeric(14,2),
	customers_refunded numeric(14,2),
	updated_at timestamp,
	unique (period_id, item_id)
);

delete from mart.f_customer_retention where period_id = EXTRACT('week' FROM '{{ ds }}'::timestamp);

insert into mart.f_customer_retention (
	new_customers_count, 
	returning_customers_count,
	refunded_customer_count,
	period_name,
	period_id,
	item_id,
	new_customers_revenue,
	returning_customers_revenue,
	customers_refunded,
	updated_at
) 
with sales as (
select 
	id, item_id, customer_id, quantity, payment_amount, week_of_year 
from 
	mart.f_sales s
inner join
	(select date_id, week_of_year from mart.d_calendar dc where week_of_year = EXTRACT('week' FROM '{{ ds }}'::timestamp)) c
	on 
		s.date_id = c.date_id 
), customers as (
	select 
		customer_id,
		item_id,
		week_of_year,
		count(1) purchases,
		sum(case when payment_amount < 0 then 1 else 0 end) refunds,
		sum(payment_amount) revenue		
	from 
		sales
	group by
		customer_id,
		item_id,
		week_of_year
), target as (
	select 
		sum(case when purchases = 1 then 1 else 0 end) new_customers_count,
		sum(case when purchases > 1 then 1 else 0 end) returning_customers_count,
		sum(case when refunds > 0 then 1 else 0 end) refunded_customer_count,
		'weekly' "period_name",
		week_of_year "period_id",
		item_id, 
		sum(case when purchases = 1 then revenue else 0 end) new_customers_revenue,
		sum(case when purchases > 1 then revenue else 0 end) returning_customers_revenue,
		sum(refunds) customers_refunded,
		'{{ ds }}'::timestamp updated_at 
	from 
		customers 
	group by 
		item_id,
		week_of_year
) select * from target order by item_id;