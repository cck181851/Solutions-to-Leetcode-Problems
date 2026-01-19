# https://leetcode.com/problems/minimum-cost-to-make-array-equal/description/
class Solution:
    def minCost(self, nums: List[int], cost: List[int]) -> int:
        def f(A):           
            res=list()
            tot=cur=0
            print(A)
            for idx,(num,c) in enumerate(A):
                if idx>0:
                    dif=abs(num-A[idx-1][0])
                    tot+=dif*cur
                res.append(tot)
                cur+=c
            return res

        left=f(sorted((i,j) for i,j in zip(nums,cost)))  
        right=f(sorted((i,j) for i,j in zip(nums,cost))[::-1])[::-1]
        return min(i+j for i,j in zip(left,right))    
