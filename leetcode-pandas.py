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
