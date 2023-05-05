drop view if exists shipping_datamart;

drop table if exists shipping_info;


-- 1.Создайте справочник стоимости доставки в страны shipping_country_rates из данных, 
-- указанных в shipping_country и shipping_country_base_rate.
-- Первичным ключом сделайте серийный id, то есть серийный идентификатор каждой строчки. 
-- Важно дать серийному ключу имя «id». Справочник должен состоять из уникальных пар полей из таблицы shipping.

drop table if exists shipping_country_rates;

create table shipping_country_rates (
	id serial,
	shipping_country text,
	shipping_country_base_rate numeric(14,3),
	primary key (id)
);

insert into shipping_country_rates (shipping_country, shipping_country_base_rate) 
select 
	distinct 
		shipping_country , 
		shipping_country_base_rate 
from 
	shipping;



-- 2.Создайте справочник тарифов доставки вендора по договору shipping_agreement из данных строки 
-- vendor_agreement_description через разделитель «:» (двоеточие без кавычек).
-- Названия полей:
--  agreementid (первичный ключ),
--  agreement_number,
--  agreement_rate,
--  agreement_commission.

drop table if exists shipping_agreement;

create table shipping_agreement (
	agreementid bigint,
	agreement_number text,
	agreement_rate numeric(14,3),
	agreement_commission numeric(14,3),
	primary key (agreementid)
);


insert into shipping_agreement 
select 
	distinct
		(regexp_split_to_array(vendor_agreement_description, ':+'))[1]::bigint as agreementid,
		(regexp_split_to_array(vendor_agreement_description, ':+'))[2]::text as agreement_number,
		(regexp_split_to_array(vendor_agreement_description, ':+'))[3]::numeric(14,3) as agreement_rate,
		(regexp_split_to_array(vendor_agreement_description, ':+'))[4]::numeric(14,3) as agreement_commission
from shipping; 



-- 3. Создайте справочник о типах доставки shipping_transfer из строки 
-- shipping_transfer_description через разделитель «:» (двоеточие без кавычек).
-- Названия полей:
--  transfer_type,
--  transfer_model,
--  shipping_transfer_rate .
-- Первичным ключом таблицы сделайте серийный id.

drop table if exists shipping_transfer;

create table shipping_transfer (
	id serial,
	transfer_type text,
	transfer_model text,
	shipping_transfer_rate numeric(14,3),
	primary key (id)
);

insert into shipping_transfer (transfer_type, transfer_model, shipping_transfer_rate) 
select 
	distinct
		(regexp_split_to_array(shipping_transfer_description, ':+'))[1]::text as transfer_type,
		(regexp_split_to_array(shipping_transfer_description, ':+'))[2]::text as transfer_model,
		shipping_transfer_rate::numeric(14,3)
from shipping; 


-- 4. Создайте таблицу shipping_info — справочник комиссий по странам с уникальными доставками shippingid.
-- Свяжите её с созданными справочниками shipping_country_rates, shipping_agreement, shipping_transfer 
-- и константной информации о доставке shipping_plan_datetime, payment_amount, vendorid.

drop table if exists shipping_info;

create table shipping_info (
	shipping_id bigint,
	vendorid bigint,
	payment_amount numeric(14,3),
	shipping_plan_datetime timestamp,
	transfer_type_id bigint,
	shipping_country_id bigint,
	agreementid bigint,
	
	foreign key(transfer_type_id) references shipping_transfer(id),
	foreign key(shipping_country_id) references shipping_country_rates(id),
	foreign key(agreementid) references shipping_agreement(agreementid)
);

insert into shipping_info 
select 
	distinct
		s.shippingid,
		s.vendorid,
		s.payment_amount ,
		s.shipping_plan_datetime,
		t.id "transfer_type_id",
		c.id "shipping_country_id",
		a.agreementid 
from 
	shipping s 
inner join
	shipping_transfer t 
	on t.transfer_type || ':' || t.transfer_model = s.shipping_transfer_description
inner join
	shipping_country_rates c 
	on c.shipping_country = s.shipping_country and c.shipping_country_base_rate = s.shipping_country_base_rate
inner join
	shipping_agreement a 
	on 1 = 1
		and (regexp_split_to_array(s.vendor_agreement_description, ':+'))[1]::bigint = a.agreementid
		and (regexp_split_to_array(s.vendor_agreement_description, ':+'))[2]::text = a.agreement_number
		and (regexp_split_to_array(s.vendor_agreement_description, ':+'))[3]::numeric(14,3) = a.agreement_rate
		and (regexp_split_to_array(s.vendor_agreement_description, ':+'))[4]::numeric(14,3) = a.agreement_commission		
;



-- 5.Создайте таблицу статусов о доставке shipping_status.
-- Включите туда информацию из лога shipping (status , state). Также добавьте туда вычислимую информацию по фактическому времени доставки shipping_start_fact_datetime и shipping_end_fact_datetime.
-- Отразите для каждого уникального shippingid его итоговое состояние доставки.

drop table if exists shipping_status;

create table shipping_status as
with having_recieved as (
select 
	distinct 
		shippingid,
		first_value(state_datetime) over (partition by shippingid order by state_datetime asc nulls last rows between unbounded preceding and unbounded following) "recieved_time"
from 
	shipping s 
where 
	state in ('recieved', 'returned')
), slv as (
select 
	s.shippingid, 
	s.status, 
	s.state,
	s.state_datetime,
	hr.recieved_time,
	first_value(s.state_datetime) over (partition by s.shippingid order by s.state_datetime asc nulls last rows between unbounded preceding and unbounded following) "first_event_time",
	last_value(s.state_datetime) over (partition by s.shippingid order by s.state_datetime asc nulls first rows between unbounded preceding and unbounded following) "final_event_time"
from 
	shipping s
left join 
	having_recieved hr
	on s.shippingid = hr.shippingid
) select 
	shippingid,
	status,
	state,
	first_event_time "shipping_start_fact_datetime",
	recieved_time "shipping_end_fact_datetime"
from 
	slv 
where 
	state_datetime = final_event_time
;



-- 6. Создайте представление shipping_datamart на основании готовых таблиц для аналитики и включите в него:
--  shippingid
--  vendorid
--  transfer_type — тип доставки из таблицы shipping_transfer
--  full_day_at_shipping — количество полных дней, в течение которых длилась доставка. Высчитывается так: shipping_end_fact_datetime -− shipping_start_fact_datetime
--  is_delay — статус, показывающий просрочена ли доставка. Высчитывается так: shipping_end_fact_datetime >> shipping_plan_datetime →→ 1; 0
--  is_shipping_finish — статус, показывающий, что доставка завершена. Если финальный status = finished →→ 1; 0
--  delay_day_at_shipping — количество дней, на которые была просрочена доставка. Высчитывается как: shipping_end_fact_datetime >> shipping_plan_datetime →→ shipping_end_fact_datetime -− shipping_plan_datetime; 0)
--  payment_amount — сумма платежа пользователя
--  vat — итоговый налог на доставку Высчитывается так: payment_amount * (shipping_country_base_rate ++ agreement_rate ++ shipping_transfer_rate)
--  profit — итоговый доход компании с доставки. Высчитывается как: payment_amount * agreement_commission

create view shipping_datamart as 
select 
	si.shipping_id "shippingid",
	si.vendorid,
	si.transfer_type_id as "transfer_type",
	shipping_end_fact_datetime - shipping_start_fact_datetime as "full_day_at_shipping",
	shipping_end_fact_datetime > shipping_plan_datetime "is_delay",
	ss.status = 'finished' as "is_shipping_finish", 
	case 	
		when shipping_end_fact_datetime > shipping_plan_datetime then shipping_end_fact_datetime - shipping_plan_datetime
		else '0'::interval
	end as "delay_day_at_shipping",	
	si.payment_amount,
	si.payment_amount * (sr.shipping_country_base_rate + sa.agreement_rate + st.shipping_transfer_rate) as "vat",
	si.payment_amount * sa.agreement_commission as "profit"
from
	shipping_info si
left join
	shipping_status ss
	on si.shipping_id = ss.shippingid
left join 
	shipping_country_rates sr
	on si.shipping_country_id = sr.id	
left join 
	shipping_agreement sa
	on si.agreementid = sa.agreementid	
left join 
	shipping_transfer st 
	on si.transfer_type_id = st.id
;







