# https://leetcode.com/problems/find-the-sum-of-the-power-of-all-subsequences/
mod=10**9+7
class Solution:
    def sumOfPower(self, nums: List[int], k: int) -> int:
        cnt=Counter(nums)
        l=len(nums)
        nums=list(sorted(set(nums))[::-1])
        
        @cache
        def f(tot,ln,idx):            
            if tot==k:                    
                return pow(2,l-ln,mod)
            if idx==len(nums) or tot>k:
                return 0            
            res=0
            for j in range(cnt[nums[idx]]+1):
                res+=f(tot+j*nums[idx],ln+j,idx+1)*comb(cnt[nums[idx]],j)
                res%=mod
            return res  

        return f(0,0,0)               
