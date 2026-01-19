# https://leetcode.com/problems/number-of-beautiful-partitions/description/
mod=10**9+7
class Solution:
    def beautifulPartitions(self, s: str, k: int, mL: int) -> int:
        P=("2","3","5","7")

        @cache
        def f(idx,rem,e):
            if idx==len(s):
                return int(rem==0 and e==0)
            if idx>len(s):
                return 0    
            if e==0:
                return (0 if s[idx] not in P else f(idx+mL-1,rem,1))%mod
            if e==1:
                a=0 if s[idx] in P else f(idx+1,rem-1,0)
                return (f(idx+1,rem,1)+a)%mod           

        return f(0,k,0)
