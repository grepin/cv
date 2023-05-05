delete from staging.user_order_log where updated_at = '{{ds}}';
delete from mart.f_sales where updated_at = '{{ds}}';
