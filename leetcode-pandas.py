import pandas as pd

"""
176. Second Highest Salary
Table: Employee

+-------------+------+
| Column Name | Type |
+-------------+------+
| id          | int  |
| salary      | int  |
+-------------+------+
id is the primary key (column with unique values) for this table.
Each row of this table contains information about the salary of an employee.
 

Write a solution to find the second highest salary from the Employee table. If there is no second highest salary, return null (return None in Pandas).
"""

import pandas as pd

#solution 1
def second_highest_salary(employee: pd.DataFrame) -> pd.DataFrame:
    data=employee.sort_values(["salary"],ascending=False)["salary"].drop_duplicates()
    return pandas.DataFrame({"SecondHighestSalary":[None if data.shape[0]<=1 else data.iloc[1]]})

#solution 2 
def second_highest_salary(employee: pd.DataFrame) -> pd.DataFrame:
    employee["rank"]=employee["salary"].rank(ascending=False,method="dense")
    data=employee.loc[lambda x:x["rank"]==2,"salary"]
    return pandas.DataFrame({"SecondHighestSalary":[data.iloc[0] if data.shape[0]>0 else None]})

#solution 3 
def second_highest_salary(employee: pd.DataFrame) -> pd.DataFrame:
    data=employee["salary"].rank(ascending=False,method="dense")
    merged=employee.assign(rank=data).loc[lambda x:x["rank"]==2,"salary"]
    return pandas.DataFrame({"SecondHighestSalary":[None if merged.shape[0]==0 else merged.iloc[0]]})

#solution 4 
def second_highest_salary(employee: pd.DataFrame) -> pd.DataFrame:
    data=employee.sort_values("salary",ascending=False)["salary"].drop_duplicates().nlargest(2)
    return pandas.DataFrame({"SecondHighestSalary":[data.iloc[1] if data.shape[0]==2 else None]})

"""
177. Nth Highest Salary
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
import pandas as pd

#solution 1
def nth_highest_salary(employee: pd.DataFrame, N: int) -> pd.DataFrame:
    data=employee["salary"].drop_duplicates().nlargest(N)
    return pandas.DataFrame({"getNthHighestSalary("+str(N)+")":[None if N<=0 or data.shape[0]<N else data.iloc[N-1]]})

#solution 2 
def nth_highest_salary(employee: pd.DataFrame, N: int) -> pd.DataFrame:
    data=employee.assign(rank=employee["salary"].rank(method="dense",ascending=False)).loc[lambda x:x["rank"]==N,"salary"]
    return pandas.DataFrame({"getNthHighestSalary("+str(N)+")":[None if data.shape[0]==0 or N<=0 else data.iloc[0]]})

#solution 3 
def nth_highest_salary(employee: pd.DataFrame, N: int) -> pd.DataFrame:
    data=employee["salary"].sort_values(ascending=False).drop_duplicates()
    return pandas.DataFrame({"getNthHighestSalary("+str(N)+")":[None if data.shape[0]<N or N<=0 else data.iloc[N-1]]})
 
"""
178. Rank Scores
Table: Scores

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| score       | decimal |
+-------------+---------+
id is the primary key (column with unique values) for this table.
Each row of this table contains the score of a game. Score is a floating point value with two decimal places.
 

Write a solution to find the rank of the scores. The ranking should be calculated according to the following rules:

The scores should be ranked from the highest to the lowest.
If there is a tie between two scores, both should have the same ranking.
After a tie, the next ranking number should be the next consecutive integer value. In other words, there should be no holes between ranks.
Return the result table ordered by score in descending order.
"""

import pandas as pd

#solution 1 
def order_scores(scores: pd.DataFrame) -> pd.DataFrame:
    scores.sort_values("score",inplace=True,axis=0,ascending=False)
    cur,prev_val=0,-1
    
    def f(row):
        nonlocal cur,prev_val
        cur,prev_val=cur+(row.score!=prev_val),row.score
        return cur
    
    return pandas.DataFrame({"score":scores["score"],"rank":scores.apply(f,axis=1)})

#solution 2 
def order_scores(scores: pd.DataFrame) -> pd.DataFrame:
    data=scores.assign(rank=scores["score"].rank(method="dense",ascending=False))
    return pandas.DataFrame({"score":data["score"],"rank":data["rank"]}).sort_values("score",ascending=False)

"""
180. Consecutive Numbers
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

import pandas as pd

#solution 1
def consecutive_numbers(logs: pd.DataFrame) -> pd.DataFrame:
    logs.sort_values("id",inplace=True)
    prev2,prev1,prev2_id,prev1_id=-2,-2,-1,-1
    
    def f(row):
        nonlocal prev2,prev1,prev2_id,prev1_id
        res=(prev2==prev1==row.num) and (prev2_id==prev1_id-1==row.id-2)
        prev2,prev1,prev2_id,prev1_id=prev1,row.num,prev1_id,row.id
        return res
    
    data=logs.assign(isCons=logs.apply(f,axis=1))
    return data.loc[lambda x:x["isCons"],["num"]].rename(
        columns={"num":"ConsecutiveNums"}).drop_duplicates()

"""
184. Department Highest Salary
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

import pandas as pd

#solution 1
def department_highest_salary(employee: pd.DataFrame, department: pd.DataFrame) -> pd.DataFrame:
    data=employee.assign(highest=employee.groupby("departmentId")["salary"].transform(max)).loc[
        lambda x:x["salary"]==x["highest"]]
    return data.merge(department,left_on="departmentId",right_on="id",how="inner")[
        ["name_y","name_x","salary"]
    ].rename(columns={"name_y":"Department","name_x":"Employee","salary":"Salary"})

#solution 2 
def department_highest_salary(employee: pd.DataFrame, department: pd.DataFrame) -> pd.DataFrame:
    data=employee.groupby(
        "departmentId"
    )["salary"].max().reset_index()
    
    merged=pandas.merge(
        employee,data,on=["departmentId","salary"],how="inner"
    )[["name","salary","departmentId"]]
    
    return pandas.merge(department,merged,left_on="id",right_on="departmentId",how="inner",suffixes=("_dep","_emp"))[
        ["name_dep","name_emp","salary"]].rename(
        columns={"name_dep":"Department","name_emp":"Employee","salary":"Salary"}
    )

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
 

Write a solution to report the fraction of players that logged in again on the day 
after the day they first logged in, rounded to 2 decimal places. In other words, 
you need to count the number of players that logged in for at least two consecutive 
days starting from their first login date, then divide that number by the total number of players.
"""

import pandas as pd

#solution 1
def gameplay_analysis(activity: pd.DataFrame) -> pd.DataFrame:
    activity["min"]=activity.groupby(
        "player_id"
    )["event_date"].transform(min)
    filtered=activity.loc[
        lambda x:(x["event_date"]-x["min"])==timedelta(days=1),"player_id"
    ].nunique()
    return pandas.DataFrame(
        {"fraction":[round(filtered/activity["player_id"].nunique(),2)]}
    )

#solution 2 
def gameplay_analysis(activity: pd.DataFrame) -> pd.DataFrame:
    data=activity.groupby(
        "player_id"
    ).min()
    
    data["event_date"]=data["event_date"]+timedelta(days=1)
    
    merged=pandas.merge(
        activity,data,on=["player_id","event_date"],how="inner"
    )["player_id"].nunique()
    
    return pandas.DataFrame(
        {"fraction":[round(merged/activity["player_id"].nunique(),2)]}
    )

"""
570. Managers with at Least 5 Direct Reports
SQL Schema
Table: Employee

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| name        | varchar |
| department  | varchar |
| managerId   | int     |
+-------------+---------+
id is the primary key (column with unique values) for this table.
Each row of this table indicates the name of an employee, their department, and the id of their manager.
If managerId is null, then the employee does not have a manager.
No employee will be the manager of themself.
 

Write a solution to find managers with at least five direct reports.

Return the result table in any order.
"""

import pandas as pd

#solution 1
def find_managers(employee: pd.DataFrame) -> pd.DataFrame:
    data=employee.groupby("managerId")["managerId"].count().loc[lambda x:x>=5].rename_axis("val")
    return employee.merge(data,how="inner",left_on="id",right_on="val")[["name"]]

#solution 2
def find_managers(employee: pd.DataFrame) -> pd.DataFrame:
    return employee.merge(
        employee.groupby("managerId").agg(counting=("id","count")).query("counting>=5"),
        left_on="id",
        right_on="managerId"
    )[["name"]]

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

import pandas as pd

#solution 1
def find_investments(insurance: pd.DataFrame) -> pd.DataFrame:
    dup=insurance[insurance.duplicated(subset=["tiv_2015"],keep=False)].pid
    sing=insurance.drop_duplicates(subset=["lat","lon"],keep=False).pid
    
    return insurance[
        lambda x:(x["pid"].isin(sing) & x["pid"].isin(dup))
    ][["tiv_2016"]].sum().to_frame("tiv_2016").round(2)

#solution 2
def find_investments(insurance: pd.DataFrame) -> pd.DataFrame:
    data_tiv_2015=insurance.groupby(
        "tiv_2015"
    )["pid"].count().loc[lambda x:x>1]
    
    lat_lon=insurance.groupby(
        ["lat","lon"]
    )["pid"].count().loc[lambda x:x==1]
    
    total_inv_2016=insurance.merge(
        data_tiv_2015,on="tiv_2015",how="inner"
    ).merge(
        lat_lon,on=["lat","lon"],how="inner"
    )["tiv_2016"].sum()
    
    return pandas.DataFrame(
        {"tiv_2016":[round(total_inv_2016,2)]}
    )

"""
602. Friend Requests II: Who Has the Most Friends
SQL Schema
Table: RequestAccepted

+----------------+---------+
| Column Name    | Type    |
+----------------+---------+
| requester_id   | int     |
| accepter_id    | int     |
| accept_date    | date    |
+----------------+---------+
(requester_id, accepter_id) is the primary key (combination of columns with unique values) for this table.
This table contains the ID of the user who sent the request, the ID of the user who received the request, and the date when the request was accepted.
 

Write a solution to find the people who have the most friends and the most friends number.

The test cases are generated so that only one person has the most friends.
"""

import pandas as pd

#solution
def most_friends(request_accepted: pd.DataFrame) -> pd.DataFrame:
    left=request_accepted.groupby("requester_id")["accepter_id"].count().rename_axis("id")
    right=request_accepted.groupby("accepter_id")["requester_id"].count().rename_axis("id")
    
    return left.add(right,fill_value=0).reset_index().rename(columns={0:"num"}).query("num==num.max()")

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

The result format is in the following example.
"""

def top_three_salaries(employee: pd.DataFrame, department: pd.DataFrame) -> pd.DataFrame:
    employee["rank"]=employee.groupby("departmentId"
    )["salary"].rank(method="dense",ascending=False)
    
    return pandas.merge(
        employee.loc[lambda x:x["rank"]<=3],department,
        how="inner",
        left_on="departmentId",
        right_on="id"
    )[["name_y","name_x","salary"]].rename(
        columns={
            "name_x":"Department",
            "name_y":"Employee",
            "salary":"Salary"
        }
    )

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

def trips_and_users(trips: pd.DataFrame, users: pd.DataFrame) -> pd.DataFrame:
    data=trips[
        (trips["request_at"]>="2013-10-01") & (trips["request_at"]<="2013-10-03")
    ]
    
    filtered=users.loc[
        lambda x:x["banned"]=="No","users_id"
    ]
    
    final=data[
        data["client_id"].isin(filtered) & (data["driver_id"].isin(filtered))
    ].assign(
        status=data["status"].apply(lambda x:1 if x!="completed" else 0)
    ).groupby("request_at")["status"].mean().reset_index()
    
    return pandas.DataFrame(
        {
            "Day":final["request_at"],
            "Cancellation Rate":final["status"].round(2)}
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

def human_traffic(stadium: pd.DataFrame) -> pd.DataFrame:
    cons,prev,n=0,-1,stadium.shape[0]
    
    def f(row):
        nonlocal cons,prev
        cons=cons+1 if row.people>=100 and row.id==prev+1 else 1 if row.people>=100 else 0
        prev=row.id
        return cons
    
    stadium["rank"]=stadium.apply(f,axis=1)
    truth=pandas.Series(
        [stadium.iloc[i,3]>=3 or 
         i+1<n and stadium.iloc[i+1,3]>=3 or 
         i+2<n and stadium.iloc[i+2,3]>=3
    for i in range(n)])
    
    return stadium.loc[truth,["id","visit_date","people"]].sort_values("visit_date")

"""
608. Tree Node
SQL Schema
Table: Tree

+-------------+------+
| Column Name | Type |
+-------------+------+
| id          | int  |
| p_id        | int  |
+-------------+------+
id is the column with unique values for this table.
Each row of this table contains information about the id of a node and the id of its parent node in a tree.
The given structure is always a valid tree.
 

Each node in the tree can be one of three types:

"Leaf": if the node is a leaf node.
"Root": if the node is the root of the tree.
"Inner": If the node is neither a leaf node nor a root node.
Write a solution to report the type of each node in the tree.

Return the result table in any order.
"""

import pandas as pd

def tree_node(tree: pd.DataFrame) -> pd.DataFrame:
    tree["type"]=np.where(pandas.isnull(tree["p_id"]),"Root",
                         (np.where(~tree["id"].isin(tree["p_id"]),"Leaf","Inner"))
                         )
    return tree[["id","type"]]

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

def sales_analysis(sales: pd.DataFrame, product: pd.DataFrame) -> pd.DataFrame:
    return sales.assign(
        first_year=sales.groupby("product_id")["year"].transform(min)
    ).query("year==first_year").iloc[:,[1,5,3,4]]

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

def market_analysis(users: pd.DataFrame, orders: pd.DataFrame, items: pd.DataFrame) -> pd.DataFrame:
    data=orders.loc[
        lambda x:x["order_date"].dt.strftime("%Y")=="2019"
    ].groupby("buyer_id")["order_id"].count()
    
    merged=users.merge(
        data,left_on="user_id",right_on="buyer_id",how="left"
    ).fillna(0)
    
    return merged[
        ["user_id","join_date","order_id"]
    ].rename(
        columns={"order_id":"orders_in_2019","user_id":"buyer_id"}
    )

"""
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

def price_at_given_date(products: pd.DataFrame) -> pd.DataFrame:
    products["latest"]=products.loc[
        lambda x:x["change_date"].dt.strftime("%Y-%m-%d")<="2019-08-16"
    ].groupby("product_id")["change_date"].transform(max)
    
    filtered=products.loc[
        lambda x:x["change_date"]==x["latest"]
    ][["product_id","new_price"]]
    
    return pandas.merge(
        products["product_id"].drop_duplicates(),filtered,on="product_id",how="left"
    ).fillna(10).rename(
        columns={"new_price":"price"}
    )

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

def immediate_food_delivery(delivery: pd.DataFrame) -> pd.DataFrame:
    data=delivery[
        delivery["order_date"]==delivery.groupby("customer_id")["order_date"].transform(min)
    ]
    x=data.loc[
        lambda x:x["order_date"]==x["customer_pref_delivery_date"]
    ].shape[0]
    
    return pandas.DataFrame(
        {"immediate_percentage":[round(100*x/data.shape[0],2)]}
    )

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

def monthly_transactions(T: pd.DataFrame) -> pd.DataFrame:
    T["approved"]=np.where(T["state"]=="approved",T["amount"],np.nan)
    T["month"]=T["trans_date"].dt.strftime("%Y-%m")
    return T.groupby(["month","country"],dropna=False).agg(
        trans_count=("amount","count"),
        approved_count=("approved","count"),
        trans_total_amount=("amount","sum"),
        approved_total_amount=("approved","sum")
    ).reset_index()

"""
1204. Last Person to Fit in the Bus
SQL Schema
Table: Queue

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| person_id   | int     |
| person_name | varchar |
| weight      | int     |
| turn        | int     |
+-------------+---------+
person_id column contains unique values.
This table has the information about all people waiting for a bus.
The person_id and turn columns will contain all numbers from 1 to n, where n is the number of rows in the table.
turn determines the order of which the people will board the bus, where turn=1 denotes the first person to board and turn=n denotes the last person to board.
weight is the weight of the person in kilograms.
 

There is a queue of people waiting to board a bus. However, the bus has a weight limit of 1000 kilograms, so there may be some people who cannot board.

Write a solution to find the person_name of the last person that can fit on the bus without exceeding the weight limit. The test cases are generated such that the first person does not exceed the weight limit.

Note that only one person can board the bus at any given turn.
"""

def last_passenger(queue: pd.DataFrame) -> pd.DataFrame:
    data=queue.sort_values("turn")
    tot_so_far=0
    
    def f(row):
        nonlocal tot_so_far
        tot_so_far+=row.weight
        return tot_so_far
    
    #data["weight"]=data.apply(f,axis=1)
    data["weight"]=data["weight"].cumsum()
    return data.loc[lambda x:x["weight"]<=1000,["person_name"]].iloc[[-1]]

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

def restaurant_growth(customer: pd.DataFrame) -> pd.DataFrame:
    merged=customer[["visited_on"]].merge(
        customer.groupby("visited_on")["amount"].sum(),on="visited_on").drop_duplicates()
    cur_tot=prev_tot=prev_el=0
    
    def f(row):
        nonlocal cur_tot,prev_tot,prev_el
        cur_tot,prev_tot,prev_el=row.amount+cur_tot,prev_tot+prev_el,row.amount
        return cur_tot,prev_tot
    
    merged[["cur_tot","prev_tot"]]=merged.apply(f,axis=1,result_type="expand")
    res=[]
    for i in range(6,merged.shape[0]):
        cur,prev=merged.iloc[i],merged.iloc[i-6]
        res+=[[cur.visited_on,(cur.cur_tot-prev.prev_tot),round((cur.cur_tot-prev.prev_tot)/7,2)]]
        
    return pandas.DataFrame(res,columns=["visited_on","amount","average_amount"])

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

def movie_rating(movies: pd.DataFrame, users: pd.DataFrame, movie_rating: pd.DataFrame) -> pd.DataFrame:
    data=pandas.merge(users,movie_rating,on="user_id").groupby("user_id")["rating"].count()
    user_with_max=users.merge(data,on="user_id").sort_values(["rating","name"],ascending=[False,True]).iloc[0,1]
    
    data2=pandas.merge(movies,movie_rating,on="movie_id").loc[
        lambda x:x["created_at"].dt.strftime("%Y-%m")=="2020-02",["movie_id","rating"]
    ].groupby("movie_id")["rating"].mean()
    movie_with_max=pandas.merge(movies,data2,on="movie_id").sort_values(["rating","title"],ascending=[False,True]).iloc[0,1]
    
    return pandas.DataFrame({"results":[user_with_max,movie_with_max]})

"""
1393. Capital Gain/Loss
SQL Schema
Table: Stocks

+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| stock_name    | varchar |
| operation     | enum    |
| operation_day | int     |
| price         | int     |
+---------------+---------+
(stock_name, operation_day) is the primary key (combination of columns with unique values) for this table.
The operation column is an ENUM (category) of type ('Sell', 'Buy')
Each row of this table indicates that the stock which has stock_name had an operation on the day operation_day with the price.
It is guaranteed that each 'Sell' operation for a stock has a corresponding 'Buy' operation in a previous day. It is also guaranteed that each 'Buy' operation for a stock has a corresponding 'Sell' operation in an upcoming day.
 

Write a solution to report the Capital gain/loss for each stock.

The Capital gain/loss of a stock is the total gain or loss after buying and selling the stock one or many times.

Return the result table in any order.
"""

def capital_gainloss(stocks: pd.DataFrame) -> pd.DataFrame:

    def helper(operation, price):
        if operation == "Buy":
            return -int(price)
        elif operation == "Sell":
            return int(price)
        
    stocks['price'] = stocks.apply(lambda x: helper(x.operation, x.price), axis=1)

    df = stocks.groupby(by='stock_name')['price'].sum().reset_index(name='capital_gain_loss')
    
    return df

"""
1934. Confirmation Rate
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

def confirmation_rate(signups: pd.DataFrame, confirmations: pd.DataFrame) -> pd.DataFrame:
    confirmations["x"]=np.where(confirmations["action"]=="confirmed",1,np.nan)
    data=confirmations.groupby("user_id").agg(
        total_count=("time_stamp","count"),
        approved_count=("x","count")
    )
    merged=pandas.merge(signups,data,on="user_id",how="left")
    merged["confirmation_rate"]=round((merged["approved_count"]/merged["total_count"]).fillna(0),2)
    return merged[["user_id","confirmation_rate"]]

