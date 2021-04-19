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
add primary key (food_id),
add cost_per_100g double;

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
    constraint part_of_plan foreign key (plan_id)
		references plan(plan_id)
        on delete cascade
        on update cascade,
	constraint meal_of foreign key (recipe_id)
		references recipe(recipe_id)
        on delete restrict
        on update cascade);
        
/* Populate with demo data */
/*Nutrients to track */
insert into daily_nut_requ (nutrient_id, requ) values ('326', 1000);
insert into daily_nut_requ (nutrient_id, requ) values ('303', 14.8);
insert into daily_nut_requ (nutrient_id, requ) values ('309', 8);
insert into daily_nut_requ (nutrient_id, requ) values ('401', 90);
insert into daily_nut_requ (nutrient_id, requ) values ('430', 50);

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
insert into plan(plan_name) values ('week 1');
set @w1_id = (select plan_id from plan where (plan_name = 'week 1'));
insert into meal (plan_id, recipe_id, num_servings) values (@w1_id, @cc_pasta_id, 2);
insert into meal (plan_id, recipe_id, num_servings) values (@w1_id, @apb_id, 4);
insert into meal (plan_id, recipe_id, num_servings) values (@w1_id, @pro_bowl_id , 5);
insert into meal (plan_id, recipe_id, num_servings) values (@w1_id, @spinach_soup_id , 2);