# https://leetcode.com/problems/maximum-strictly-increasing-cells-in-a-matrix/description/
class Solution:
    def maxIncreasingCells(self, mat: List[List[int]]) -> int:
        d=defaultdict(list)
        m,n=len(mat),len(mat[0])
        A=[0]*(m+n)
        for i in range(m):
            for j in range(n):
                d[mat[i][j]].append((i,j))

        for key,vals in sorted(d.items()):
            nw=Counter()
            for r,c in vals:
                a,b=A[r],A[m+c]
                nw[r]=max(nw[r],max(a,b)+1)
                nw[m+c]=max(nw[m+c],max(a,b)+1)
            for r,c in vals:
                A[r]=max(A[r],nw[r])
                A[m+c]=max(A[m+c],nw[m+c])

        return max(A)            
