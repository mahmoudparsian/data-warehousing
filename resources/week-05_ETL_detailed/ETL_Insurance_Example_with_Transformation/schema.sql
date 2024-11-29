use test;
drop table insurance_from_etl2;
create table `insurance_from_etl2` (
`index` int,
`age` int,
`sex` text,
`bmi` double,
`children` int,
`smoker` text,
`region` text,
`charges` double,
`bmi_indicator` text,
`age_group` text
);

select * from insurance_from_etl2;

select count(*) from insurance_from_etl2;

select * from insurance_from_etl2;

