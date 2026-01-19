# https://leetcode.com/problems/minimum-cost-to-split-an-array/description/
class Solution:
    def minCost(self, nums: List[int], k: int) -> int:
        @cache
        def f(idx):
            if idx==len(nums):
                return 0
            cur = 0
            cnt = Counter()
            res = math.inf
            for j in range(idx,len(nums)):
                p = nums[j]
                cur += 1 if cnt[p] > 1 else 2 if cnt[p] == 1 else 0
                cnt[p] += 1
                res = min(res,k+cur+f(j+1))
            return res

        return f(0)   
