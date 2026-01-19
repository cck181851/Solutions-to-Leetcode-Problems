# https://leetcode.com/problems/number-of-pairs-satisfying-inequality/description/
from sortedcontainers import SortedList 
class Solution:
    def numberOfPairs(self, nums1: List[int], nums2: List[int], diff: int) -> int:
        A=SortedList()
        res=0
        for i in [i-j for i,j in zip(nums1,nums2)]:
            res+=bisect_right(A,i+diff)            
            A.add(i)            
        return res    
        
