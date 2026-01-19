# https://leetcode.com/problems/minimum-operations-to-form-subsequence-with-target-sum/
class Solution:
    def minOperations(self, nums: List[int], target: int) -> int:
        cnt=[0 for _ in range(32)]
        freq=Counter()
        for i in range(31,-1,-1):
            t=1<<i
            if t<=target:
                target-=t
                cnt[i]+=1
        for i in nums:
            q=0
            while i>1:
                q+=1
                i//=2 
            freq[q]+=1

        def f(j,i,freq):
            cur=0
            while j>i:
                freq[j]-=1
                j-=1
                freq[j]+=2    
                cur+=1
            return cur         

        res=0        
        for i in range(32):            
            if cnt[i]:
                if not freq[i]:
                    for j in range(i+1,32):                        
                        if freq[j]:
                            res+=f(j,i,freq)                            
                            break
                    else:
                        return -1  
                freq[i]-=1                                          
            freq[i+1]+=freq[i]//2            
        return res   
