"""
175. Combine Two Tables

SQL Schema
Table: Person

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| personId    | int     |
| lastName    | varchar |
| firstName   | varchar |
+-------------+---------+
personId is the primary key (column with unique values) for this table.
This table contains information about the ID of some persons and their first and last names.
 

Table: Address

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| addressId   | int     |
| personId    | int     |
| city        | varchar |
| state       | varchar |
+-------------+---------+
addressId is the primary key (column with unique values) for this table.
Each row of this table contains information about the city and state of one person with ID = PersonId.
 

Write a solution to report the first name, last name, city, and state of each person in the Person table. If the address of a personId is not present in the Address table, report null instead.

Return the result table in any order.
"""
  
select firstName,lastName,city,state from person left join address using (personId)

"""
176. Second Highest Salary

SQL Schema
Table: Employee

+-------------+------+
| Column Name | Type |
+-------------+------+
| id          | int  |
| salary      | int  |
+-------------+------+
id is the primary key (column with unique values) for this table.
Each row of this table contains information about the salary of an employee.
 

Write a solution to find the second highest distinct salary from the Employee table. If there is no second highest salary, return null (return None in Pandas).

The result format is in the following example.
"""

with helper as (select distinct salary  from employee order by salary desc limit 1 offset 1)
select max(salary) as "SecondHighestSalary" from helper

"""

177. Nth Highest Salary

SQL Schema
Table: Employee

+-------------+------+
| Column Name | Type |
+-------------+------+
| id          | int  |
| salary      | int  |
+-------------+------+
id is the primary key (column with unique values) for this table.
Each row of this table contains information about the salary of an employee.
 

Write a solution to find the nth highest salary from the Employee table. If there is no nth highest salary, return null.

The result format is in the following example.

"""

CREATE FUNCTION getNthHighestSalary(N INT) RETURNS INT
BEGIN
DECLARE M INT; 
SET M=N-1;
  RETURN (
    SELECT DISTINCT Salary FROM Employee ORDER BY Salary DESC LIMIT 1 OFFSET M
  );
END

"""  

180. Consecutive Numbers
SQL Schema
Table: Logs

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| num         | varchar |
+-------------+---------+
In SQL, id is the primary key for this table.
id is an autoincrement column.
 

Find all numbers that appear at least three times consecutively.

Return the result table in any order.

The result format is in the following example.
"""

select distinct num as "ConsecutiveNums" from
(select 
    num,
    @rank:=if(@prev_id=id-1 and @prev_num=num,@rank+1,1) as "rank",
    @prev_id:=id as "prev_id",
    @prev_num:=num as "prev_num"
from (select id,num from logs order by id) a,(select @prev_num:=-1,@prev_id:=-1,@rank:=0) b ) c 
where c.rank>=3

"""

184. Department Highest Salary

SQL Schema
Table: Employee

+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| id           | int     |
| name         | varchar |
| salary       | int     |
| departmentId | int     |
+--------------+---------+
id is the primary key (column with unique values) for this table.
departmentId is a foreign key (reference columns) of the ID from the Department table.
Each row of this table indicates the ID, name, and salary of an employee. It also contains the ID of their department.
 

Table: Department

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| name        | varchar |
+-------------+---------+
id is the primary key (column with unique values) for this table. It is guaranteed that department name is not NULL.
Each row of this table indicates the ID of a department and its name.
 

Write a solution to find employees who have the highest salary in each of the departments.

Return the result table in any order.

"""

with helper as 
    (select *,rank() over(partition by departmentId order by salary desc) as "idx" 
     from employee)
select 
    b.name as "Department",
    a.name as "Employee",a.salary as "Salary" 
from helper a
inner join department b on a.departmentId=b.id 
where a.idx=1

"""
  
185. Department Top Three Salaries

SQL Schema
Table: Employee

+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| id           | int     |
| name         | varchar |
| salary       | int     |
| departmentId | int     |
+--------------+---------+
id is the primary key (column with unique values) for this table.
departmentId is a foreign key (reference column) of the ID from the Department table.
Each row of this table indicates the ID, name, and salary of an employee. It also contains the ID of their department.
 

Table: Department

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| name        | varchar |
+-------------+---------+
id is the primary key (column with unique values) for this table.
Each row of this table indicates the ID of a department and its name.
 

A company's executives are interested in seeing who earns the most money in each of the company's departments. A high earner in a department is an employee who has a salary in the top three unique salaries for that department.

Write a solution to find the employees who are high earners in each of the departments.

Return the result table in any order.

"""

with helper as (
    select *,
        dense_rank() over(partition by departmentId order by salary desc) as "rnk" 
    from employee),
helper2 as (
    select * 
    from helper 
    where rnk<=3)
select 
    department.name as "Department",
    helper2.name as "Employee",
    helper2.salary as "Salary"
from helper2 
inner join department on helper2.departmentId=department.id

""" 

262. Trips and Users

SQL Schema
Table: Trips

+-------------+----------+
| Column Name | Type     |
+-------------+----------+
| id          | int      |
| client_id   | int      |
| driver_id   | int      |
| city_id     | int      |
| status      | enum     |
| request_at  | varchar  |     
+-------------+----------+
id is the primary key (column with unique values) for this table.
The table holds all taxi trips. Each trip has a unique id, while client_id and driver_id are foreign keys to the users_id at the Users table.
Status is an ENUM (category) type of ('completed', 'cancelled_by_driver', 'cancelled_by_client').
 

Table: Users

+-------------+----------+
| Column Name | Type     |
+-------------+----------+
| users_id    | int      |
| banned      | enum     |
| role        | enum     |
+-------------+----------+
users_id is the primary key (column with unique values) for this table.
The table holds all users. Each user has a unique users_id, and role is an ENUM type of ('client', 'driver', 'partner').
banned is an ENUM (category) type of ('Yes', 'No').
 

The cancellation rate is computed by dividing the number of canceled (by client or driver) requests with unbanned users by the total number of requests with unbanned users on that day.

Write a solution to find the cancellation rate of requests with unbanned users (both client and driver must not be banned) each day between "2013-10-01" and "2013-10-03". Round Cancellation Rate to two decimal points.

Return the result table in any order.

"""

with data as (
    select * 
    from trips 
    where "2013-10-01"<=request_at and request_at<="2013-10-03"
),
valid as (
    select * 
    from data 
    where client_id not in (select users_id from users where banned="Yes") and 
    driver_id not in (select users_id from users where banned="Yes")
)
select 
    request_at as "Day",
    round(sum(if(status!="completed",1,0))/count(*),2) as "Cancellation Rate" 
from valid
group by request_at 

"""
  
550. Game Play Analysis IV

SQL Schema
Table: Activity

+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| player_id    | int     |
| device_id    | int     |
| event_date   | date    |
| games_played | int     |
+--------------+---------+
(player_id, event_date) is the primary key (combination of columns with unique values) of this table.
This table shows the activity of players of some games.
Each row is a record of a player who logged in and played a number of games (possibly 0) before logging out on someday using some device.
 

Write a solution to report the fraction of players that logged in again on the day after the day they first logged in, rounded to 2 decimal places. In other words, you need to count the number of players that logged in for at least two consecutive days starting from their first login date, then divide that number by the total number of players.

"""

with helper as 
    (select player_id,
            min(event_date) as "first_logged_in" 
    from activity 
     group by player_id),
helper2 as 
    (select count(distinct a.player_id) 
     from activity a 
     inner join helper h on a.player_id=h.player_id and datediff(a.event_date,h.first_logged_in)=1)
select 
    round((select * from helper2)/count(distinct player_id),2) as "fraction" 
from activity

"""

585. Investments in 2016

SQL Schema
Table: Insurance

+-------------+-------+
| Column Name | Type  |
+-------------+-------+
| pid         | int   |
| tiv_2015    | float |
| tiv_2016    | float |
| lat         | float |
| lon         | float |
+-------------+-------+
pid is the primary key (column with unique values) for this table.
Each row of this table contains information about one policy where:
pid is the policyholder's policy ID.
tiv_2015 is the total investment value in 2015 and tiv_2016 is the total investment value in 2016.
lat is the latitude of the policy holder's city. It's guaranteed that lat is not NULL.
lon is the longitude of the policy holder's city. It's guaranteed that lon is not NULL.
 

Write a solution to report the sum of all total investment values in 2016 tiv_2016, for all policyholders who:

have the same tiv_2015 value as one or more other policyholders, and
are not located in the same city as any other policyholder (i.e., the (lat, lon) attribute pairs must be unique).
Round tiv_2016 to two decimal places.

"""

#find pid's and their total investment in 2015
with helper as 
    (select pid,lat,lon,sum(tiv_2015) as "tot" 
     from insurance group by pid),
#find pid's with total investing in 2015 which is same as one of the other investors'
helper2 as 
    (select pid,lat,lon from helper h 
     where (select count(*) from helper where h.tot=tot)>1
    )
#We have valid pid's,now find the sum
select 
    round(sum(tiv_2016),2) as "tiv_2016" 
from insurance 
where pid in (
    select pid from helper2 h 
    where (
        select count(*) from insurance where lon=h.lon and lat=h.lat
    )=1
)

"""
  
601. Human Traffic of Stadium

SQL Schema
Table: Stadium

+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| id            | int     |
| visit_date    | date    |
| people        | int     |
+---------------+---------+
visit_date is the column with unique values for this table.
Each row of this table contains the visit date and visit id to the stadium with the number of people during the visit.
As the id increases, the date increases as well.
 

Write a solution to display the records with three or more rows with consecutive id's, and the number of people is greater than or equal to 100 for each.

Return the result table ordered by visit_date in ascending order.

"""

with helper as (
    select 
        id,
        visit_date,
        people,
        @cons:=if(people>=100 and @prev_id=id-1,@cons+1,if(people>=100,1,0)) as "cons",
        @prev_id:=id as "prev_id"
    from stadium,
    (select @cons:=0,@prev_id:=0) init),
helper2 as (
    select 
        id,
        visit_date,
        people,
        cons,
        lead(cons,2) over() as "lead_2",
        lead(cons,1) over() as "lead_1" 
    from helper)
select 
    id,
    visit_date,
    people 
from helper2 
where lead_2>=3 or lead_1>=3 or cons>=3

"""
1045. Customers Who Bought All Products

SQL Schema
Table: Customer

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| customer_id | int     |
| product_key | int     |
+-------------+---------+
This table may contain duplicates rows. 
customer_id is not NULL.
product_key is a foreign key (reference column) to Product table.
 

Table: Product

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| product_key | int     |
+-------------+---------+
product_key is the primary key (column with unique values) for this table.
 

Write a solution to report the customer ids from the Customer table that bought all the products in the Product table.

Return the result table in any order.  
"""

select 
    customer_id 
    from customer 
    group by customer_id 
    having count(distinct product_key)=
        (select 
            count(distinct product_key) 
         from product
        )

"""
1070. Product Sales Analysis III

SQL Schema
Table: Sales

+-------------+-------+
| Column Name | Type  |
+-------------+-------+
| sale_id     | int   |
| product_id  | int   |
| year        | int   |
| quantity    | int   |
| price       | int   |
+-------------+-------+
(sale_id, year) is the primary key (combination of columns with unique values) of this table.
product_id is a foreign key (reference column) to Product table.
Each row of this table shows a sale on the product product_id in a certain year.
Note that the price is per unit.
 

Table: Product

+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| product_id   | int     |
| product_name | varchar |
+--------------+---------+
product_id is the primary key (column with unique values) of this table.
Each row of this table indicates the product name of each product.
 

Write a solution to select the product id, year, quantity, and price for the first year of every product sold.

Return the resulting table in any order.
"""

select 
    product_id,
    year as first_year,
    quantity,
    price 
from sales 
where (product_id,year) in 
        (select 
            product_id,
            min(year) 
        from sales 
        group by product_id)


"""
1158. Market Analysis I

SQL Schema
Table: Users

+----------------+---------+
| Column Name    | Type    |
+----------------+---------+
| user_id        | int     |
| join_date      | date    |
| favorite_brand | varchar |
+----------------+---------+
user_id is the primary key (column with unique values) of this table.
This table has the info of the users of an online shopping website where users can sell and buy items.
 

Table: Orders

+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| order_id      | int     |
| order_date    | date    |
| item_id       | int     |
| buyer_id      | int     |
| seller_id     | int     |
+---------------+---------+
order_id is the primary key (column with unique values) of this table.
item_id is a foreign key (reference column) to the Items table.
buyer_id and seller_id are foreign keys to the Users table.
 

Table: Items

+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| item_id       | int     |
| item_brand    | varchar |
+---------------+---------+
item_id is the primary key (column with unique values) of this table.
 

Write a solution to find for each user, the join date and the number of orders they made as a buyer in 2019.

Return the result table in any order.  
"""

select 
    user_id as "buyer_id",
    join_date,
    sum(if(order_id is null or year(order_date)!=2019,0,1)) as "orders_in_2019"
from users 
left join orders on orders.buyer_id=users.user_id
group by user_id

"""
1164. Product Price at a Given Date

SQL Schema
Table: Products

+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| product_id    | int     |
| new_price     | int     |
| change_date   | date    |
+---------------+---------+
(product_id, change_date) is the primary key (combination of columns with unique values) of this table.
Each row of this table indicates that the price of some product was changed to a new price at some date.
 

Write a solution to find the prices of all products on 2019-08-16. Assume the price of all products before any change is 10.

Return the result table in any order.  
"""

with helper as (select product_id,new_price,rank() over(partition by product_id order by change_date desc) as "rnk"
from products where change_date<="2019-08-16")
select distinct
    p.product_id,
    if(h.new_price is null,10,h.new_price) as "price"
from products p 
left join helper h on h.product_id=p.product_id and h.rnk=1

"""
1174. Immediate Food Delivery II

SQL Schema
Table: Delivery

+-----------------------------+---------+
| Column Name                 | Type    |
+-----------------------------+---------+
| delivery_id                 | int     |
| customer_id                 | int     |
| order_date                  | date    |
| customer_pref_delivery_date | date    |
+-----------------------------+---------+
delivery_id is the column of unique values of this table.
The table holds information about food delivery to customers that make orders at some date and specify a preferred delivery date (on the same order date or after it).
 

If the customer's preferred delivery date is the same as the order date, then the order is called immediate; otherwise, it is called scheduled.

The first order of a customer is the order with the earliest order date that the customer made. It is guaranteed that a customer has precisely one first order.

Write a solution to find the percentage of immediate orders in the first orders of all customers, rounded to 2 decimal places.
"""

with helper as 
    (select 
        customer_id,
        min(order_date) "first" 
     from delivery 
     group by customer_id),
helper2 as (
    select 
        d.customer_id,
        d.order_date,
        d.customer_pref_delivery_date 
    from delivery d 
    inner join helper h on d.customer_id=h.customer_id and d.order_date=h.first
)
select 
    round(100*sum(
            if(order_date=customer_pref_delivery_date,1,0))/count(*),
          2) as "immediate_percentage"
from helper2

"""

1193. Monthly Transactions I
SQL Schema
Table: Transactions

+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| id            | int     |
| country       | varchar |
| state         | enum    |
| amount        | int     |
| trans_date    | date    |
+---------------+---------+
id is the primary key of this table.
The table has information about incoming transactions.
The state column is an enum of type ["approved", "declined"].
 

Write an SQL query to find for each month and country, the number of transactions and their total amount, the number of approved transactions and their total amount.

Return the result table in any order.
  
"""

select 
    left(trans_date,7) as "month", 
    country,
    count(*) as "trans_count",
    sum(if(state="approved",1,0)) as "approved_count",
    sum(amount) as "trans_total_amount",
    sum(if(state="approved",amount,0)) as "approved_total_amount"
from transactions group by country,left(trans_date,7)

"""

1321. Restaurant Growth

SQL Schema
Table: Customer

+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| customer_id   | int     |
| name          | varchar |
| visited_on    | date    |
| amount        | int     |
+---------------+---------+
In SQL,(customer_id, visited_on) is the primary key for this table.
This table contains data about customer transactions in a restaurant.
visited_on is the date on which the customer with ID (customer_id) has visited the restaurant.
amount is the total paid by a customer.
 

You are the restaurant owner and you want to analyze a possible expansion (there will be at least one customer every day).

Compute the moving average of how much the customer paid in a seven days window (i.e., current day + 6 days before). average_amount should be rounded to two decimal places.

Return the result table ordered by visited_on in ascending order.
"""

with helper as (
    select 
        visited_on,
        @cur_tot:=@cur_tot+amount as "cur_tot",
        @prev_tot:=@prev_tot+@prev_el as "prev_tot",
        @prev_el:=amount as "prev_el" 
        from (
            select 
                visited_on,
                sum(amount) as "amount" 
            from customer 
            group by visited_on 
            order by visited_on) init,
            (
                select 
                    @cur_tot:=0,
                    @prev_tot:=0,
                    @prev_el:=0
            ) init2
)
select 
    h1.visited_on,
    h1.cur_tot-h2.prev_tot as "amount",
    round((h1.cur_tot-h2.prev_tot)/7,2) as "average_amount"
from helper h1 
inner join helper h2 on datediff(h1.visited_on,h2.visited_on)=6


"""
  
1341. Movie Rating
SQL Schema
Table: Movies

+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| movie_id      | int     |
| title         | varchar |
+---------------+---------+
movie_id is the primary key (column with unique values) for this table.
title is the name of the movie.
 

Table: Users

+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| user_id       | int     |
| name          | varchar |
+---------------+---------+
user_id is the primary key (column with unique values) for this table.
The column 'name' has unique values.
Table: MovieRating

+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| movie_id      | int     |
| user_id       | int     |
| rating        | int     |
| created_at    | date    |
+---------------+---------+
(movie_id, user_id) is the primary key (column with unique values) for this table.
This table contains the rating of a movie by a user in their review.
created_at is the user's review date. 
 

Write a solution to:

Find the name of the user who has rated the greatest number of movies. In case of a tie, return the lexicographically smaller user name.
Find the movie name with the highest average rating in February 2020. In case of a tie, return the lexicographically smaller movie name.
"""

with helper as (select name,count(*) as tot from users inner join movieRating using (user_id) group by user_id),
helper2 as (select *,avg(rating) as "avg" from movies inner join movieRating using (movie_id) where left(created_at,7)="2020-02" group by movies.movie_id)
                
(select name as "results" from helper order by tot desc,name asc limit 1 )
union all
(select title as "results" from helper2 order by avg desc,title asc limit 1)

"""
  1907. Count Salary Categories

SQL Schema
Table: Accounts

+-------------+------+
| Column Name | Type |
+-------------+------+
| account_id  | int  |
| income      | int  |
+-------------+------+
account_id is the primary key (column with unique values) for this table.
Each row contains information about the monthly income for one bank account.
 

Write a solution to calculate the number of bank accounts for each salary category. The salary categories are:

"Low Salary": All the salaries strictly less than $20000.
"Average Salary": All the salaries in the inclusive range [$20000, $50000].
"High Salary": All the salaries strictly greater than $50000.
The result table must contain all three categories. If there are no accounts in a category, return 0.

Return the result table in any order.
"""

(select "Low Salary" as category,sum(if(income<20000,1,0)) as "accounts_count" from accounts)
union 
(select "Average Salary" as category,sum(if(income between 20000 and 50000,1,0)) as "accounts_count" from accounts)
union 
(select "High Salary" as category,sum(if(income>50000,1,0)) as "accounts_count" from accounts)

"""
1934. Confirmation Rate
Medium

907

81

Add to List

Share
SQL Schema
Table: Signups

+----------------+----------+
| Column Name    | Type     |
+----------------+----------+
| user_id        | int      |
| time_stamp     | datetime |
+----------------+----------+
user_id is the column of unique values for this table.
Each row contains information about the signup time for the user with ID user_id.
 

Table: Confirmations

+----------------+----------+
| Column Name    | Type     |
+----------------+----------+
| user_id        | int      |
| time_stamp     | datetime |
| action         | ENUM     |
+----------------+----------+
(user_id, time_stamp) is the primary key (combination of columns with unique values) for this table.
user_id is a foreign key (reference column) to the Signups table.
action is an ENUM (category) of the type ('confirmed', 'timeout')
Each row of this table indicates that the user with ID user_id requested a confirmation message at time_stamp and that confirmation message was either confirmed ('confirmed') or expired without confirming ('timeout').
 

The confirmation rate of a user is the number of 'confirmed' messages divided by the total number of requested confirmation messages. The confirmation rate of a user that did not request any confirmation messages is 0. Round the confirmation rate to two decimal places.

Write a solution to find the confirmation rate of each user.

Return the result table in any order.  
  
"""

select  
    user_id,
    round(sum(if(action="confirmed",1,0))/count(*),2) as "confirmation_rate"
from signups
left join confirmations
using (user_id)
group by signups.user_id

"""
  1327. List the Products Ordered in a Period

SQL Schema
Table: Products

+------------------+---------+
| Column Name      | Type    |
+------------------+---------+
| product_id       | int     |
| product_name     | varchar |
| product_category | varchar |
+------------------+---------+
product_id is the primary key (column with unique values) for this table.
This table contains data about the company's products.
 

Table: Orders

+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| product_id    | int     |
| order_date    | date    |
| unit          | int     |
+---------------+---------+
This table may have duplicate rows.
product_id is a foreign key (reference column) to the Products table.
unit is the number of products ordered in order_date.
 

Write a solution to get the names of products that have at least 100 units ordered in February 2020 and their amount.

Return the result table in any order.
"""

with helper as 
    (select
        product_id,
     sum(unit) as "unit" from orders 
     where order_date>"2020-02-00" and order_date<"2020-03-00" 
     group by product_id 
having sum(unit)>=100)
select 
    product_name,
    unit 
from products 
inner join helper 
using(product_id)

