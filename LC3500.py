class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        acc1=list(accumulate(nums))
        acc2=list(accumulate(cost))

        @cache
        def f(right):
            if right==-1:
                return 0
            res=math.inf
            for left in range(right,-1,-1):                
                a=acc1[right]*(acc2[right]-(0 if left==0 else acc2[left-1]))
                b=k*(acc2[-1]-(0 if left==0 else acc2[left-1]))
                res=min(res,a+b+f(left-1))
            return res

        return f(len(nums)-1)   
