use test;
drop table insurance_from_etl;
create table insurance_from_etl (
index int,
age int,
sex text,
bmi double,
children int,
smoker text,
region text,
charges double);

select * from insurance_from_etl;

select count(*) from insurance_from_etl;

select * from insurance_from_etl;

