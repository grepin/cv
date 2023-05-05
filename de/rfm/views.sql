
drop view if exists analysis.orderitems;
create view analysis.orderitems as select * from production.orderitems;

drop view if exists analysis.orders;
create view analysis.orders as select * from production.orders where order_ts >= '2022-01-01';

drop view if exists analysis.orderstatuses;
create view analysis.orderstatuses as select * from production.orderstatuses;

drop view if exists analysis.products;
create view analysis.products as select * from production.products;

drop view if exists analysis.users;
create view analysis.users as select * from production.users;

