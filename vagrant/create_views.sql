create view count_by_date as 
select 
    time::date as date,
    count(*) as log_count
from log 
group by date;

create view error_by_date as
select 
    time::date as date,
    count(*) as error_count 
from log 
where status like '4%' or status like '5%' 
group by date;

create view error_rate_by_date as
select 
    c.date, 
    1.0 * error_count/log_count as error_rate 
from count_by_date as c join error_by_date as e on c.date = e.date;