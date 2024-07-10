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

