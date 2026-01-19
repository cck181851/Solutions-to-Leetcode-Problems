# https://leetcode.com/problems/paths-in-matrix-whose-sum-is-divisible-by-k/description/
mod=10**9+7
class Solution:
    def numberOfPaths(self, grid: List[List[int]], k: int) -> int:
        m,n=len(grid), len(grid[0])

        @cache
        def f(i,j,t):
            if i==m or j==n:
                return 0
            t=(t+grid[i][j])%k    
            if i==m-1 and j==n-1:
                return int(t==0)
            return (f(i+1,j,t)+f(i,j+1,t))%mod   

        return f(0,0,0)       
