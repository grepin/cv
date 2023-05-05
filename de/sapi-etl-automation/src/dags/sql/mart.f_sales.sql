insert into mart.f_sales (date_id, item_id, customer_id, city_id, quantity, payment_amount, status, updated_at)
select 
    dc.date_id, 
    item_id, 
    customer_id, 
    city_id, 
    quantity, 
    case 
        when status = 'refunded' then payment_amount * -1
        else payment_amount
    end payment_amount,
    status,
    updated_at
from 
    staging.user_order_log uol
left join mart.d_calendar as dc on uol.date_time::Date = dc.date_actual
where uol.date_time::Date = '{{ds}}';