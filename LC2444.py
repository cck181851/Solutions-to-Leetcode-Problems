# https://leetcode.com/problems/count-subarrays-with-fixed-bounds/description/
class Solution:
    def countSubarrays(self, nums: List[int], minK: int, maxK: int) -> int:
        def f(A):
            mk=mx=-1
            res=0
            for idx,i in enumerate(A):
                if i==minK:mk=idx
                if i==maxK:mx=idx
                if mk!=-1 and mx!=-1:res+=min(mk,mx)+1
            return res     

        cur=list()
        total=list()
        for i in nums+[math.inf]:
            if minK<=i<=maxK:
                cur.append(i)    
            else:
                total.append(cur.copy())
                cur=list()

        return sum(f(A) for A in total)  
