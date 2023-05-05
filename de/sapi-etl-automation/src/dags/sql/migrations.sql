alter table staging.user_order_log add column if not exists status varchar(8);
alter table staging.user_order_log add column if not exists updated_at timestamp;
alter table mart.f_sales add column if not exists status varchar(8);
alter table mart.f_sales add column if not exists updated_at timestamp;
