drop database if exists meal_plan;
create database meal_plan
character set'latin1'
collate 'latin1_swedish_ci';

drop table if exists meal_plan.nutrient;
create table meal_plan.nutrient 
	as (select Nutr_No as nutrient_id,
	nutrdesc as nutrient_name,
    units as units from usda.nutr_def);


drop table if exists meal_plan.nutrient_data;
create table meal_plan.nutrient_data
	as (select Nutr_No as nutrient_id,
    ndb_no as food_id,
    nutr_val as amt from usda.nut_data);

drop table if exists meal_plan.food_item;
create table meal_plan.food_item
	as (select ndb_no as food_id,
	Long_Desc as food_name from usda.food_des);
use meal_plan;


alter table nutrient 
add primary key (nutrient_id);

alter table food_item 
add primary key (food_id);

alter table nutrient_data
modify column nutrient_id varchar(4),
add primary key (food_id, nutrient_id),
add foreign key (food_id) references food_item(food_id),
add foreign key (nutrient_id) references nutrient(nutrient_id);


drop table if exists daily_nut_requ;
create table daily_nut_requ(
	nutrient_id varchar(4) not null,
    requ decimal(13,3) not null,
    constraint dnr_pk primary key 
    (nutrient_id),
	constraint requ_of foreign key (nutrient_id)
		references nutrient(nutrient_id)
        on delete restrict 
        on update cascade);
drop table if exists plan;
create table plan(
	plan_id int  not null auto_increment,
    plan_name varchar(300) not null, 
    num_days double not null,
    constraint plan_pk primary key 
		(plan_id));

drop table if exists recipe;
create table recipe(
	recipe_id int  not null auto_increment,
    recipe_name varchar(300) not null,
    constraint recipe_pk primary key 
		(recipe_id));

drop table if exists ingredient;
create table ingredient(
	food_id varchar(5) not null,
    recipe_id int not null,
    amount_in_grams double not null,
    constraint ing_pk primary key (food_id, recipe_id),
    constraint of_food foreign key (food_id)
		references food_item(food_id)
        on delete restrict
        on update cascade,
	constraint part_of_recipe foreign key (recipe_id)
		references recipe(recipe_id)
        on delete cascade
        on update cascade);
        
drop table if exists meal;
create table meal(
	plan_id int not null,
    recipe_id int not null,
    num_servings double not null, 
    constraint meal_pk primary key (plan_id, recipe_id),
    constraint part_of_plan foreign key (plan_id)
		references plan(plan_id)
        on delete cascade
        on update cascade,
	constraint meal_of foreign key (recipe_id)
		references recipe(recipe_id)
        on delete cascade
        on update cascade);
	
/* procedures */

drop procedure if exists search_nutrient;
create procedure search_nutrient (in nid nvarchar(4))
	select nutrient_id, nutrient_name, units from nutrient where nutrient_id like nid;

drop procedure if exists search_food_item;
create procedure search_food_item(in fid nvarchar(5))
	select food_id, food_name from food_item where food_id like fid;

drop procedure if exists search_recipe;
create procedure search_recipe(in rid varchar(5))
	select recipe_id, recipe_name from recipe where recipe_id like rid;
    
drop procedure if exists remove_recipe;
create procedure remove_recipe(in rid varchar(5))
	delete from recipe where recipe_id = rid;
    
drop procedure if exists insert_recipe;
DELIMITER //
create procedure insert_recipe(in rname varchar(200), out rid int)
begin
	insert into recipe (recipe_name) values (rname);
    select recipe_id from recipe where recipe_name = rname;
END //
DELIMITER ;
drop procedure if exists search_plan;
create procedure search_plan(in pid varchar(5))
	select plan_id, plan_name, num_days from plan where plan_id like pid;

drop procedure if exists remove_plan;
create procedure remove_plan(in pid varchar(5))
	delete from plan where plan_id like pid;

drop procedure if exists insert_plan;
DELIMITER //
create procedure insert_plan(in pname varchar(200), in days int, out pid int)
begin
	insert into plan (plan_name, num_days) values (pname, days);
    select plan_id from plan where plan_name = pname;
end //
DELIMITER ;
drop procedure if exists search_meal;
create procedure search_meal(in pid varchar(5), in rid varchar(5))
	select * from meal where plan_id like pid and recipe_id like rid;

drop procedure if exists search_ingredient;
create procedure search_ingredient(in fid varchar(5), in rid varchar(5))
	select * from ingredient where food_id like fid and recipe_id like rid;
    
drop procedure if exists remove_ingredient;
create procedure remove_ingredient(in fid varchar(5), in rid varchar(5))
	delete from ingredient where food_id = fid and recipe_id = rid;

drop procedure if exists add_ingredient;
create procedure add_ingredient(in fid varchar(5), in rid varchar(5), in amt double)
	insert into ingredient(food_id, recipe_id, amount_in_grams) values (fid, rid, amt);
    
drop procedure if exists search_nutrient_data;
create procedure search_nutrient_data(in fid varchar(5), in nid varchar(5))
	select * from nutrient_data where food_id like fid and nutrient_id like nid;
    
drop procedure if exists search_daily_requ;
create procedure search_daily_requ(in nid varchar(5))
	select n.nutrient_id, n.nutrient_name, d.requ, n.units from daily_nut_requ as d natural join nutrient as n where nutrient_id = nid;

drop procedure if exists get_nutrients_to_track;
create procedure get_nutrients_to_track()
	select n.nutrient_id, n.nutrient_name, d.requ, n.units from daily_nut_requ as d natural join nutrient as n;
    
drop procedure if exists add_nutrients_to_track;
create procedure add_nutrients_to_track(in nid varchar(5), in amt double)
	insert into daily_nut_requ (nutrient_id, requ) values (nid, amt);

drop procedure if exists remove_nutrients_to_track;
create procedure remove_nutrients_to_track(in nid varchar(5))
	delete from daily_nut_requ where (nutrient_id = nid);
    
drop procedure if exists add_meal;
create procedure add_meal(in rid varchar(5), in pid varchar(5), in amt int)
	insert into meal (recipe_id, plan_id, num_servings) values (rid, pid, amt);
    
drop procedure if exists remove_meal;
create procedure remove_meal(in rid varchar(5), in pid varchar(5))
	delete from meal where recipe_id = rid and plan_id = pid;
    
/* Populate with demo data */
/*Nutrients to track */
insert into daily_nut_requ (nutrient_id, requ) values ('326', 1000);
insert into daily_nut_requ (nutrient_id, requ) values ('303', 14.8);
insert into daily_nut_requ (nutrient_id, requ) values ('309', 8);
insert into daily_nut_requ (nutrient_id, requ) values ('401', 90);
insert into daily_nut_requ (nutrient_id, requ) values ('430', 50);
insert into daily_nut_requ (nutrient_id, requ) values ('208', 1500);

/*Recipes*/
insert into recipe (recipe_name) values ('panini');
set @panini_id = (select recipe_id from recipe where (recipe_name = 'panini'));
insert into ingredient (food_id, recipe_id, amount_in_grams) values ('02044', @panini_id , 5);
insert into ingredient (food_id, recipe_id, amount_in_grams) values ('02047', @panini_id , 5);
insert into ingredient (food_id, recipe_id, amount_in_grams) values ('11529', @panini_id , 100);
insert into ingredient (food_id, recipe_id, amount_in_grams) values ('18060', @panini_id , 100);
insert into ingredient (food_id, recipe_id, amount_in_grams) values ('01026', @panini_id , 50);

insert into recipe (recipe_name) values ('probiotic bowl');
set @pro_bowl_id = (select recipe_id from recipe where (recipe_name = 'probiotic bowl'));
insert into ingredient (food_id, recipe_id, amount_in_grams) values ('16113', @pro_bowl_id , 50);
insert into ingredient (food_id, recipe_id, amount_in_grams) values ('01116', @pro_bowl_id , 180);
insert into ingredient (food_id, recipe_id, amount_in_grams) values ('20037', @pro_bowl_id , 130);
insert into ingredient (food_id, recipe_id, amount_in_grams) values ('04047', @pro_bowl_id , 3);

insert into recipe (recipe_name) values ('spinach walnut soup');
set @spinach_soup_id = (select recipe_id from recipe where (recipe_name = 'spinach walnut soup'));
insert into ingredient (food_id, recipe_id, amount_in_grams) values ('11854', @spinach_soup_id , 300);
insert into ingredient (food_id, recipe_id, amount_in_grams) values ('11286', @spinach_soup_id , 180);
insert into ingredient (food_id, recipe_id, amount_in_grams) values ('12155', @spinach_soup_id, 50);
insert into ingredient (food_id, recipe_id, amount_in_grams) values ('11215', @spinach_soup_id , 4);
insert into ingredient (food_id, recipe_id, amount_in_grams) values ('04047', @spinach_soup_id , 18);

insert into recipe (recipe_name) values ('apples and peanut butter');
set @apb_id = (select recipe_id from recipe where (recipe_name = 'apples and peanut butter'));
insert into ingredient (food_id, recipe_id, amount_in_grams) values ('09003', @apb_id , 200);
insert into ingredient (food_id, recipe_id, amount_in_grams) values ('16097', @apb_id , 50);

insert into recipe (recipe_name) values ('chickpea cream pasta');
set @cc_pasta_id = (select recipe_id from recipe where (recipe_name = 'chickpea cream pasta'));
insert into ingredient (food_id, recipe_id, amount_in_grams) values ('16157', @cc_pasta_id , 71);
insert into ingredient (food_id, recipe_id, amount_in_grams) values ('01001', @cc_pasta_id , 30);
insert into ingredient (food_id, recipe_id, amount_in_grams) values ('20091', @cc_pasta_id , 200);
insert into ingredient (food_id, recipe_id, amount_in_grams) values ('11215', @cc_pasta_id , 30);

/*Plans */
insert into plan(plan_name, num_days) values ('week 1', 7);
set @w1_id = (select plan_id from plan where (plan_name = 'week 1'));
insert into meal (plan_id, recipe_id, num_servings) values (@w1_id, @cc_pasta_id, 2);
insert into meal (plan_id, recipe_id, num_servings) values (@w1_id, @apb_id, 4);
insert into meal (plan_id, recipe_id, num_servings) values (@w1_id, @pro_bowl_id , 5);
insert into meal (plan_id, recipe_id, num_servings) values (@w1_id, @spinach_soup_id , 2);