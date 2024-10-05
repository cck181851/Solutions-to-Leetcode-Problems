from sortedcontainers import SortedList
import itertools, functools, bisect 

"""
1579. Remove Max Number of Edges to Keep Graph Fully Traversable
Alice and Bob have an undirected graph of n nodes and three types of edges:

Type 1: Can be traversed by Alice only.
Type 2: Can be traversed by Bob only.
Type 3: Can be traversed by both Alice and Bob.
Given an array edges where edges[i] = [typei, ui, vi] represents a bidirectional edge of type typei between nodes ui and vi, find the maximum number of edges you can remove so that after removing the edges, the graph can still be fully traversed by both Alice and Bob. The graph is fully traversed by Alice and Bob if starting from any node, they can reach all other nodes.

Return the maximum number of edges you can remove, or return -1 if Alice and Bob cannot fully traverse the graph.
"""

class UnionFind:
    def __init__(self, n):
        self.count = n                
        self.parent = list(range(n)) 
        self.rank = [1]*n            
        
    def find(self, p):
        while p != self.parent[p]: 
            p=self.parent[p]
        return self.parent[p]
    
    def union(self, p, q):
        prt, qrt = self.find(p), self.find(q)
        if prt == qrt: return False
        self.count -= 1 
        if self.rank[prt] > self.rank[qrt]: prt, qrt = qrt, prt
        self.parent[prt] = qrt
        self.rank[qrt] += self.rank[prt] 
        return True
    
        
class Solution:
    def maxNumEdgesToRemove(self, n: int, edges: List[List[int]]) -> int:
        ufa = UnionFind(n) 
        ufb = UnionFind(n) 
        
        ans = 0
        edges.sort(reverse=True) 
        for t, u, v in edges: 
            u, v = u-1, v-1
            if t == 3: ans += not (ufa.union(u, v) and ufb.union(u, v)) 
            elif t == 2: ans += not ufb.union(u, v)                     
            else: ans += not ufa.union(u, v)                            
        return ans if ufa.count == 1 and ufb.count == 1 else -1
                

"""
1671. Minimum Number of Removals to Make Mountain Array
You may recall that an array arr is a mountain array if and only if:

arr.length >= 3
There exists some index i (0-indexed) with 0 < i < arr.length - 1 such that:
arr[0] < arr[1] < ... < arr[i - 1] < arr[i]
arr[i] > arr[i + 1] > ... > arr[arr.length - 1]
Given an integer array nums​​​, return the minimum number of elements to remove to make nums​​​ a mountain array.
"""

class Solution:
    def minimumMountainRemovals(self, nums: List[int]) -> int:
        def f(A):
            res,B=[],[]
            for num in A:
                if not B or num>B[-1]:
                    B+=[num]
                    res+=[len(B)]
                else:
                    idx=bisect_left(B,num)
                    B[idx]=num
                    res+=[idx+1]
            return res
        
        A,B=f(nums),f(nums[::-1])[::-1]
        mx=max([A[i]+B[i] for i in range(len(nums)) if A[i]>1 and B[i]>1] or [0])
        return len(nums)-mx+1


"""
1751. Maximum Number of Events That Can Be Attended II
You are given an array of events where events[i] = [startDayi, endDayi, valuei]. The ith event starts at startDayi and ends at endDayi, and if you attend this event, you will receive a value of valuei. You are also given an integer k which represents the maximum number of events you can attend.

You can only attend one event at a time. If you choose to attend an event, you must attend the entire event. Note that the end day is inclusive: that is, you cannot attend two events where one of them starts and the other ends on the same day.

Return the maximum sum of values that you can receive by attending events.
"""

class Solution:
    def maxValue(self, events: List[List[int]], k: int) -> int:
        events.sort()
        
        @cache
        def y(idx):
            return bisect_left(events,[events[idx][1]+1])
        
        @cache
        def f(idx,rem):
            if rem<0:
                return -math.inf
            if idx==len(events):
                return 0
            return max(f(y(idx),rem-1)+events[idx][2],f(idx+1,rem))
        return f(0,k)

"""
1766. Tree of Coprimes
There is a tree (i.e., a connected, undirected graph that has no cycles) consisting of n nodes numbered from 0 to n - 1 and exactly n - 1 edges. Each node has a value associated with it, and the root of the tree is node 0.

To represent this tree, you are given an integer array nums and a 2D array edges. Each nums[i] represents the ith node's value, and each edges[j] = [uj, vj] represents an edge between nodes uj and vj in the tree.

Two values x and y are coprime if gcd(x, y) == 1 where gcd(x, y) is the greatest common divisor of x and y.

An ancestor of a node i is any other node on the shortest path from node i to the root. A node is not considered an ancestor of itself.

Return an array ans of size n, where ans[i] is the closest ancestor to node i such that nums[i] and nums[ans[i]] are coprime, or -1 if there is no such ancestor.
"""

#solution
class Solution:
    def getCoprimes(self, nums: List[int], edges: List[List[int]]) -> List[int]:
        d={i:[j for j in range(51) if gcd(i,j)==1] for i in range(51)}
                            
        tree=defaultdict(list)
        for a,b in edges:
            tree[a].append(b)
            tree[b].append(a)
            
        res=[-1]*(len(nums))
                
        def f(node,pars,level,par):
            val,cur_res=nums[node],-1
            for dd in d[val]:
                if pars[dd] and pars[dd][-1][0]>cur_res:
                    cur_res=pars[dd][-1][0]
                    res[node]=pars[dd][-1][1]
            pars[val].append([level,node])
            for child in tree[node]:
                if child==par:continue
                f(child,pars,level+1,node)
            pars[val].pop()
            
        f(0,[[] for _ in range(51)],0,-1)
            
        return res
            
"""
2458. Height of Binary Tree After Subtree Removal Queries

You are given the root of a binary tree with n nodes. Each node is assigned a unique value from 1 to n. You are also given an array queries of size m.

You have to perform m independent queries on the tree where in the ith query you do the following:

Remove the subtree rooted at the node with the value queries[i] from the tree. It is guaranteed that queries[i] will not be equal to the value of the root.
Return an array answer of size m where answer[i] is the height of the tree after performing the ith query.

Note:

The queries are independent, so the tree returns to its initial state after each query.
The height of a tree is the number of edges in the longest simple path from the root to some node in the tree
"""

class Solution:
    def treeQueries(self, root: Optional[TreeNode], queries: List[int]) -> List[int]:
        d=defaultdict(list)
        level_map={}
        
        def f(node,level):
            if not node:
                return 0
            mx=1
            level_map[node.val]=level
            for child in [node.left,node.right]:
                if child is None:continue
                h=f(child,level+1)
                d[level].append([node.val,child.val,h+1])
                mx=max(mx,h+1)
            d[level]=sorted(d[level],key=lambda x:-x[2])[:3]
            return mx
        
        f(root,0)
        res=[]
        for q in queries:
            level=level_map[q]-1
            mx=-1
            for node,child,h in d[level]:
                if child==q:continue
                mx=max(mx,h)
            res+=[max(level,mx+level-1)]
        return res
                
"""
1938. Maximum Genetic Difference Query

There is a rooted tree consisting of n nodes numbered 0 to n - 1. Each node's number denotes its unique genetic value (i.e. the genetic value of node x is x). The genetic difference between two genetic values is defined as the bitwise-XOR of their values. You are given the integer array parents, where parents[i] is the parent for node i. If node x is the root of the tree, then parents[x] == -1.

You are also given the array queries where queries[i] = [nodei, vali]. For each query i, find the maximum genetic difference between vali and pi, where pi is the genetic value of any node that is on the path between nodei and the root (including nodei and the root). More formally, you want to maximize vali XOR pi.

Return an array ans where ans[i] is the answer to the ith query.
"""

class TrieNode:
    def __init__(self):
        self.children={}
        self.freq=0
    
class Trie:
    def __init__(self):
        self.root=TrieNode()
        
    def add(self,num,f):
        cur=self.root
        for i in range(18,-1,-1):
            bit=(num>>i)&1
            if bit not in cur.children:
                cur.children[bit]=TrieNode()
            cur=cur.children[bit]
            cur.freq+=f
            
    def getMax(self,num):
        cur,val=self.root,0
        for i in range(18,-1,-1):
            bit=(num>>i)&1
            if bit^1 in cur.children and cur.children[bit^1].freq>0:
                val+=1<<i
                cur=cur.children[bit^1]
            elif bit^0 in cur.children and cur.children[bit^0].freq>0:
                cur=cur.children[bit^0]
        return val

class Solution:
    def maxGeneticDifference(self, parents: List[int], queries: List[List[int]]) -> List[int]:
        t=Trie()
        tree=defaultdict(list)
        d=defaultdict(list)
        for idx,[a,b] in enumerate(queries):
            d[a]+=[[b,idx]]
        ans=[-1]*len(queries)
        
        for child,par in enumerate(parents):
            tree[par]+=[child]
        
        
        def dfs(node):
            t.add(node,1)
            for val,idx in d[node]:
                ans[idx]=t.getMax(val)
            for child in tree[node]:
                dfs(child)
            t.add(node,-1)
            
        dfs([i for i in range(len(parents)) if parents[i]==-1][0])
        return ans

"""
2163. Minimum Difference in Sums After Removal of Elements

You are given a 0-indexed integer array nums consisting of 3 * n elements.

You are allowed to remove any subsequence of elements of size exactly n from nums. The remaining 2 * n elements will be divided into two equal parts:

The first n elements belonging to the first part and their sum is sumfirst.
The next n elements belonging to the second part and their sum is sumsecond.
The difference in sums of the two parts is denoted as sumfirst - sumsecond.

For example, if sumfirst = 3 and sumsecond = 2, their difference is 1.
Similarly, if sumfirst = 2 and sumsecond = 3, their difference is -1.
Return the minimum difference possible between the sums of the two parts after the removal of n elements.
"""

class Solution:
    def minimumDifference(self, nums: List[int]) -> int:
        m=len(nums)
        A,q,tot=[0]*m,[],0
        for i in range(2*m//3):
            tot+=nums[i]
            heappush(q,-nums[i])
            if len(q)>m//3:
                tot+=heappop(q)
            A[i]=tot
        B,q,tot=[0]*m,[],0
        for i in range(m-1,m//3-1,-1):
            tot+=nums[i]
            heappush(q,nums[i])
            if len(q)>m//3:
                tot-=heappop(q)
            B[i]=tot
        return min(A[i]-B[i+1] for i in range(m//3-1,2*m//3))

"""
2179. Count Good Triplets in an Array

You are given two 0-indexed arrays nums1 and nums2 of length n, both of which are permutations of [0, 1, ..., n - 1].

A good triplet is a set of 3 distinct values which are present in increasing order by position both in nums1 and nums2. In other words, if we consider pos1v as the index of the value v in nums1 and pos2v as the index of the value v in nums2, then a good triplet will be a set (x, y, z) where 0 <= x, y, z <= n - 1, such that pos1x < pos1y < pos1z and pos2x < pos2y < pos2z.

Return the total number of good triplets.
"""

class BIT:
    def __init__(self,n):
        self.tree=[0]*(n+1)
        
    def add(self,val,x):
        val+=1
        while val<len(self.tree):
            self.tree[val]+=x
            val+=val&(-val)
        
    def get(self,val):
        val,res=val+1,0
        while val>0:
            res+=self.tree[val]
            val-=val&(-val)
        return res
        
class Solution:
    def goodTriplets(self, nums1: List[int], nums2: List[int]) -> int:
        res,n=0,len(nums2)
        left,right=BIT(n),BIT(n)
        
        for i in nums2:
            right.add(i,1)
            
        idx_map=defaultdict(list)
        for idx,i in enumerate(nums2):
            idx_map[i]+=[idx]
            
        for i in nums1:
            idx=idx_map[i].pop()
            right.add(idx,-1)
            x=left.get(idx-1)
            y=right.get(n-1)-right.get(idx)
            res+=x*y
            left.add(idx,1)
            
        return res


"""
2272. Substring With Largest Variance

The variance of a string is defined as the largest difference between the number of occurrences of any 2 characters present in the string. Note the two characters may or may not be the same.

Given a string s consisting of lowercase English letters only, return the largest variance possible among all substrings of s.

A substring is a contiguous sequence of characters within a string.
"""

class Solution:
    def largestVariance(self, s: str) -> int:
        def f(x,y):
            cnt=Counter()
            left=leftMin=leftCur=res=cur=0
            for idx,i in enumerate(s):
                if i in [x,y]:cnt[i]+=1
                cur+=1 if i==x else -1 if i==y else 0
                while left<idx and (s[left] not in [x,y] or cnt[s[left]]>1):
                    ch=s[left]
                    leftCur+=1 if ch==x else -1 if ch==y else 0
                    leftMin=min(leftMin,leftCur)
                    if s[left] in [x,y]:cnt[s[left]]-=1
                    left+=1
                if len(cnt)==2:
                    res=max(res,cur-leftMin)
            return res
        
        A=set(s)
        return max([f(x,y) for x in A for y in A if x!=y],default=0)

"""
2440. Create Components With Same Value

There is an undirected tree with n nodes labeled from 0 to n - 1.

You are given a 0-indexed integer array nums of length n where nums[i] represents the value of the ith node. You are also given a 2D integer array edges of length n - 1 where edges[i] = [ai, bi] indicates that there is an edge between nodes ai and bi in the tree.

You are allowed to delete some edges, splitting the tree into multiple connected components. Let the value of a component be the sum of all nums[i] for which node i is in the component.

Return the maximum number of edges you can delete, such that every connected component in the tree has the same value.
"""

class Solution:
    def componentValue(self, nums: List[int], edges: List[List[int]]) -> int:
        tree=defaultdict(list)
        for a,b in edges:
            tree[a]+=[b]
            tree[b]+=[a]
            
        def f(node,par,tar):
            cur=nums[node]
            for child in tree[node]:
                if child==par:continue
                cur+=f(child,node,tar)
            return 0 if cur==tar else cur
        
        sm=sum(nums)
        for i in range(len(nums),0,-1):
            if sm%i:continue
            tar=sm//i
            if f(0,-1,tar)==0:return i-1
        return 0

"""
2444. Count Subarrays With Fixed Bounds

You are given an integer array nums and two integers minK and maxK.

A fixed-bound subarray of nums is a subarray that satisfies the following conditions:

The minimum value in the subarray is equal to minK.
The maximum value in the subarray is equal to maxK.
Return the number of fixed-bound subarrays.

A subarray is a contiguous part of an array.
"""

class Solution:
    def countSubarrays(self, nums: List[int], minK: int, maxK: int) -> int:
        res=0
        for a in [nums]:
            cnt=Counter()
            left=start=0
            for idx,i in enumerate(a):
                if i in [minK,maxK]:
                    cnt[i]+=1
                elif i<minK or i>maxK:
                    cnt=Counter()
                    left=start=idx+1
                    continue
                while left<idx and not (a[left] in [minK,maxK] and cnt[a[left]]<=1):
                    cnt[a[left]]-=1
                    left+=1
                if cnt[minK]>0 and cnt[maxK]>0:
                    res+=left-start+1                
        return res if minK<=maxK else 0

"""
2458. Height of Binary Tree After Subtree Removal Queries

You are given the root of a binary tree with n nodes. Each node is assigned a unique value from 1 to n. You are also given an array queries of size m.

You have to perform m independent queries on the tree where in the ith query you do the following:

Remove the subtree rooted at the node with the value queries[i] from the tree. It is guaranteed that queries[i] will not be equal to the value of the root.
Return an array answer of size m where answer[i] is the height of the tree after performing the ith query.

Note:

The queries are independent, so the tree returns to its initial state after each query.
The height of a tree is the number of edges in the longest simple path from the root to some node in the tree.
"""

class Solution:
    def treeQueries(self, root: Optional[TreeNode], queries: List[int]) -> List[int]:
        d=defaultdict(list)
        level_map={}
        
        def f(node,level):
            if not node:
                return 0
            mx=1
            level_map[node.val]=level
            for child in [node.left,node.right]:
                if child is None:continue
                h=f(child,level+1)
                d[level].append([node.val,child.val,h+1])
                mx=max(mx,h+1)
            d[level]=sorted(d[level],key=lambda x:-x[2])[:3]
            return mx
        
        f(root,0)
        res=[]
        for q in queries:
            level=level_map[q]-1
            mx=-1
            for node,child,h in d[level]:
                if child==q:continue
                mx=max(mx,h)
            res+=[max(level,mx+level-1)]
        return res

"""
2503. Maximum Number of Points From Grid Queries

You are given an m x n integer matrix grid and an array queries of size k.

Find an array answer of size k such that for each integer queries[i] you start in the top left cell of the matrix and repeat the following process:

If queries[i] is strictly greater than the value of the current cell that you are in, then you get one point if it is your first time visiting this cell, and you can move to any adjacent cell in all 4 directions: up, down, left, and right.
Otherwise, you do not get any points, and you end this process.
After the process, answer[i] is the maximum number of points you can get. Note that for each query you are allowed to visit the same cell multiple times.

Return the resulting array answer.
"""

class Solution:
    def maxPoints(self, grid: List[List[int]], queries: List[int]) -> List[int]:
        m,n=len(grid),len(grid[0])
        par=[j+i*n for i in range(m) for j in range(n)]
        rank=[0 for i in range(m*n)]
        
        def find(x):
            while x!=par[x]:
                x=par[x]
            return x
        
        def union(x,y):
            px,py=find(x),find(y)
            if px==py:return
            if rank[py]>rank[py]:px,py=py,px
            par[py]=px
            rank[px]+=rank[py]
            
        A=sorted((grid[x][y],x,y) for x in range(m) for y in range(n))
        res=[0]*len(queries)
        p=0
        seen=[[0]*n for _ in range(m)]
        for val,idx in sorted((val,idx) for idx,val in enumerate(queries)):
            while p<len(A) and A[p][0]<val:
                x,y=A[p][1],A[p][2]
                seen[x][y]=1
                rank[y+x*n]+=1
                for xx,yy in [(x+1,y),(x,y+1),(x-1,y),(x,y-1)]:
                    if 0<=xx<m and 0<=yy<n and seen[xx][yy]:
                        union(xx*n+yy,x*n+y)
                p+=1
            res[idx]=rank[find(0)]
        return res

"""
2518. Number of Great Partitions

You are given an array nums consisting of positive integers and an integer k.

Partition the array into two ordered groups such that each element is in exactly one group. A partition is called great if the sum of elements of each group is greater than or equal to k.

Return the number of distinct great partitions. Since the answer may be too large, return it modulo 109 + 7.

Two partitions are considered distinct if some element nums[i] is in different groups in the two partitions.
"""

class Solution:
    def countPartitions(self, nums: List[int], k: int) -> int:
        mod=10**9+7
        
        @cache
        def f(idx,tot):
            if idx==len(nums):
                return 1
            res=f(idx+1,tot)
            if tot+nums[idx]<k:res+=f(idx+1,tot+nums[idx])
            return res%mod
        
        return (pow(2,len(nums),mod)-2*f(0,0))%mod if sum(nums)>=2*k else 0

"""
2547. Minimum Cost to Split an Array

You are given an integer array nums and an integer k.

Split the array into some number of non-empty subarrays. The cost of a split is the sum of the importance value of each subarray in the split.

Let trimmed(subarray) be the version of the subarray where all numbers which appear only once are removed.

For example, trimmed([3,1,2,4,3,4]) = [3,4,3,4].
The importance value of a subarray is k + trimmed(subarray).length.

For example, if a subarray is [1,2,3,3,3,4,4], then trimmed([1,2,3,3,3,4,4]) = [3,3,3,4,4].The importance value of this subarray will be k + 5.
Return the minimum possible cost of a split of nums.

A subarray is a contiguous non-empty sequence of elements within an array.
"""

class Solution:
    def minCost(self, nums: List[int], k: int) -> int:
        @cache
        def f(idx):
            if idx==len(nums):
                return 0
            A,B=set(),set()
            res,tot=math.inf,0
            for j in range(idx,len(nums)):
                x=nums[j]
                if x not in A and x not in B:
                    A.add(x)
                elif x in A:
                    tot+=2
                    A.remove(x)
                    B.add(x)
                else:
                    tot+=1
                res=min(res,tot+k+f(j+1))
            return res
        return f(0)

"""
2577. Minimum Time to Visit a Cell In a Grid

You are given a m x n matrix grid consisting of non-negative integers where grid[row][col] represents the minimum time required to be able to visit the cell (row, col), which means you can visit the cell (row, col) only when the time you visit it is greater than or equal to grid[row][col].

You are standing in the top-left cell of the matrix in the 0th second, and you must move to any adjacent cell in the four directions: up, down, left, and right. Each move you make takes 1 second.

Return the minimum time required in which you can visit the bottom-right cell of the matrix. If you cannot visit the bottom-right cell, then return -1.
"""

class Solution:
    def minimumTime(self, grid: List[List[int]]) -> int:
        m,n=len(grid),len(grid[0])
        seen=[[math.inf]*n for _ in range(m)]
        q=[(0,0,0)]
        while q:
            t,r,c=heappop(q)
            if [r,c]==[m-1,n-1]:
                return t
            A=[(r+1,c),(r,c+1),(r-1,c),(r,c-1)]
            h=any(0<=a<m and 0<=b<n and grid[a][b]<=(1+t) for a,b in A)
            for nr,nc in A:
                if 0<=nr<m and 0<=nc<n and h:
                    nt=1+t if grid[nr][nc]<=(1+t) else grid[nr][nc]+(((grid[nr][nc]-t)%2)^1)
                    if nt<seen[nr][nc]:
                        heappush(q,[nt,nr,nc])
                        seen[nr][nc]=nt
        return -1

"""
2584. Split the Array to Make Coprime Products

You are given a 0-indexed integer array nums of length n.

A split at an index i where 0 <= i <= n - 2 is called valid if the product of the first i + 1 elements and the product of the remaining elements are coprime.

For example, if nums = [2, 3, 3], then a split at the index i = 0 is valid because 2 and 9 are coprime, while a split at the index i = 1 is not valid because 6 and 3 are not coprime. A split at the index i = 2 is not valid because i == n - 1.
Return the smallest index i at which the array can be split validly or -1 if there is no such split.

Two values val1 and val2 are coprime if gcd(val1, val2) == 1 where gcd(val1, val2) is the greatest common divisor of val1 and val2.
"""

primes=[i for i in range(1000001)]
for i in range(2,len(primes)):
    j=i+i
    while j<len(primes):
        if primes[j]==j:
            primes[j]=i
        j+=i

class Solution:
    def findValidSplit(self, nums: List[int]) -> int:
        def getDiv(n):
            cnt=Counter()
            while n>1:
                p=primes[n]
                cnt[p]+=1
                n//=p
            return cnt
        
        left,right,cur=Counter(),Counter(),0
        for num in nums:
            for i,j in getDiv(num).items():
                right[i]+=j
                
        for idx,num in enumerate(nums):
            for i,j in getDiv(num).items():
                if left[i]>0 and right[i]==j:
                    cur-=1
                if left[i]==0 and right[i]>j:
                    cur+=1
                left[i]+=j
                right[i]-=j
            if not cur and idx!=len(nums)-1:
                return idx
        return -1

"""
2709. Greatest Common Divisor Traversal

You are given a 0-indexed integer array nums, and you are allowed to traverse between its indices. You can traverse between index i and index j, i != j, if and only if gcd(nums[i], nums[j]) > 1, where gcd is the greatest common divisor.

Your task is to determine if for every pair of indices i and j in nums, where i < j, there exists a sequence of traversals that can take us from i to j.

Return true if it is possible to traverse between all such pairs of indices, or false otherwise.
"""

class Solution:
    def canTraverseAllPairs(self, nums: List[int]) -> bool:
        primes=[i for i in range(100001)]
        for i in range(2,100001):
            j=i+i
            while j<len(primes):
                if primes[j]==j:primes[j]=i
                j+=i        
        
        
        if 1 in nums:
            return False if nums!=[1] else True

        par={}
        rank={}
        
        def find(x):
            if x not in par:
                par[x],rank[x]=x,1
            while x!=par[x]:
                x=par[x]
            return par[x]
        
        def union(x,y):
            px,py=find(x),find(y)
            if rank[px]<rank[py]:
                px,py=py,px
            if px!=py:
                rank[px]+=rank[py]
                par[py]=px
            
        for num in nums:
            prev=num
            while num>=2:
                prime=primes[num]
                union(prev,prime)
                prev=primes[num]
                while not num%prime:
                    num//=prime
                
        return len(set(find(x) for x in nums))==1


"""
2719. Count of Integers

You are given two numeric strings num1 and num2 and two integers max_sum and min_sum. We denote an integer x to be good if:

num1 <= x <= num2
min_sum <= digit_sum(x) <= max_sum.
Return the number of good integers. Since the answer may be large, return it modulo 109 + 7.

Note that digit_sum(x) denotes the sum of the digits of x.
"""

class Solution:
    def count(self, num1: str, num2: str, min_sum: int, max_sum: int) -> int:
        mod=10**9+7
        def helper(limit):
            A=[int(i) for i in str(limit)]
            @cache
            def f(idx,tot,state):
                if tot>max_sum:
                    return 0
                if idx==len(A):
                    return tot>=min_sum
                res=0
                for i in range(10):
                    if state==0 and i>A[idx]:break
                    res+=f(idx+1,tot+i,1 if state==1 else i<A[idx])
                return res%mod
            return f(0,0,0)
        return (helper(int(num2))-helper(int(num1)-1))%mod

"""
2736. Maximum Sum Queries

You are given two 0-indexed integer arrays nums1 and nums2, each of length n, and a 1-indexed 2D array queries where queries[i] = [xi, yi].

For the ith query, find the maximum value of nums1[j] + nums2[j] among all indices j (0 <= j < n), where nums1[j] >= xi and nums2[j] >= yi, or -1 if there is no j satisfying the constraints.

Return an array answer where answer[i] is the answer to the ith query.
"""

class Solution:
    def maximumSumQueries(self, nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
        n=len(nums2)
        tree=[-1]*4*n
        
        def add(left,right,idx,pos,val):
            if left==right:
                tree[idx]=val
                return
            mid=(left+right)//2
            if pos<=mid:
                add(left,mid,idx*2+1,pos,val)
            else:
                add(mid+1,right,idx*2+2,pos,val)
            tree[idx]=max(tree[idx*2+1],tree[idx*2+2])
            
        def query(left,right,qleft,qright,idx):
            if qright<left or right<qleft:
                return -1
            if qleft<=left<=right<=qright:
                return tree[idx]
            mid=(left+right)//2
            i=query(left,mid,qleft,qright,idx*2+1)
            j=query(mid+1,right,qleft,qright,idx*2+2)
            return max(i,j)
        
        B=sorted(nums2)
        c=defaultdict(list)
        for idx,i in enumerate(B):
            c[i].append(idx)
        
        A=sorted([i,idx] for idx,i in enumerate(nums1))
        res,p=[-1]*len(queries),len(A)-1
        for idx,[x,y] in sorted(enumerate(queries),key=lambda x:-x[1][0]):
            while p>=0 and A[p][0]>=x:
                ind=A[p][1]
                p-=1
                add(0,n,0,c[nums2[ind]].pop(),nums1[ind]+nums2[ind])
            tmp_idx=bisect_left(B,y)
            res[idx]=query(0,n,tmp_idx,n,0)
        return res

"""
2781. Length of the Longest Valid Substring

You are given a string word and an array of strings forbidden.

A string is called valid if none of its substrings are present in forbidden.

Return the length of the longest valid substring of the string word.

A substring is a contiguous sequence of characters in a string, possibly empty.
"""

class Solution:
    def longestValidSubstring(self, word: str, forbidden: List[str]) -> int:
        A=[-1]*len(word)
        mod=10**18+7
        forbidden=set(sum(pow(26,idx,mod)*(ord(i)-96)%mod 
                for idx,i in enumerate(f[::-1])) for f in forbidden)
        
        for i in range(len(word)):
            cur=0
            for j in range(10):
                if i-j<0:break
                cur+=(ord(word[i-j])-96)*pow(26,j,mod)
                cur%=mod
                if cur in forbidden:
                    A[i]=max(A[i],i-j+1)
                    break
        
        res=left=0
        for i in range(len(word)):
            left=max(left,A[i])
            res=max(res,i-left+1)
        return res
                

"""
2842. Count K-Subsequences of a String With Maximum Beauty

You are given a string s and an integer k.

A k-subsequence is a subsequence of s, having length k, and all its characters are unique, i.e., every character occurs once.

Let f(c) denote the number of times the character c occurs in s.

The beauty of a k-subsequence is the sum of f(c) for every character c in the k-subsequence.

For example, consider s = "abbbdd" and k = 2:

f('a') = 1, f('b') = 3, f('d') = 2
Some k-subsequences of s are:
"abbbdd" -> "ab" having a beauty of f('a') + f('b') = 4
"abbbdd" -> "ad" having a beauty of f('a') + f('d') = 3
"abbbdd" -> "bd" having a beauty of f('b') + f('d') = 5
Return an integer denoting the number of k-subsequences whose beauty is the maximum among all k-subsequences. Since the answer may be too large, return it modulo 109 + 7.

A subsequence of a string is a new string formed from the original string by deleting some (possibly none) of the characters without disturbing the relative positions of the remaining characters.
"""

class Solution:
    def countKSubsequencesWithMaxBeauty(self, s: str, k: int) -> int:
        if k>len(set(s)):
            return 0 
        cnt=Counter(s)
        A=sorted(cnt.items(),key=lambda x:-x[1])
        tar=sum(i[1] for i in A[:k])
        mod=10**9+7
        
        def f(idx,x):
            if x<=0:
                return x==0
            if idx==len(A):
                return int(x==0)
            take=f(idx+1,x-1)*cnt[A[idx][0]]
            go=f(idx+1,x)
            return (take+go if idx+1<len(A) and A[idx+1][1]==A[idx][1] else take)%mod
        
        return f(0,k)


"""
2867. Count Valid Paths in a Tree

There is an undirected tree with n nodes labeled from 1 to n. You are given the integer n and a 2D integer array edges of length n - 1, where edges[i] = [ui, vi] indicates that there is an edge between nodes ui and vi in the tree.

Return the number of valid paths in the tree.

A path (a, b) is valid if there exists exactly one prime number among the node labels in the path from a to b.

Note that:

The path (a, b) is a sequence of distinct nodes starting with node a and ending with node b such that every two adjacent nodes in the sequence share an edge in the tree.
Path (a, b) and path (b, a) are considered the same and counted only once.
"""

class Solution:
    def countPaths(self, n: int, edges: List[List[int]]) -> int:
        A=list(range(100001))
        for i in range(2,len(A)):
            j=i+i
            while j<len(A):
                if A[j]==j:A[j]=i
                j+=i
        primes=set(i for i in A if i==A[i] and i>=2)
        
        
        par,rank=list(range(n+1)),[1]*(n+1)
        
        def find(x):
            while x!=par[x]:
                x=par[x]
            return par[x]
        
        def union(x,y):
            px,py=find(x),find(y)
            if px==py:return
            if rank[py]>rank[px]:px,py=py,px
            rank[px]+=rank[py]
            par[py]=px
        
        res,d=0,defaultdict(list)
        for a,b in edges:
            if a not in primes and b not in primes:
                union(a,b)
            if a in primes and b not in primes:
                d[a]+=[b]
            if b in primes and a not in primes:
                d[b]+=[a]
                
        for i in range(n+1):
            if i not in primes:continue
            tot=0
            for j in d[i]:
                x=rank[find(j)]
                res+=tot*x
                tot+=x
            res+=tot
        return res


"""
2935. Maximum Strong Pair XOR II

You are given a 0-indexed integer array nums. A pair of integers x and y is called a strong pair if it satisfies the condition:

|x - y| <= min(x, y)
You need to select two integers from nums such that they form a strong pair and their bitwise XOR is the maximum among all strong pairs in the array.

Return the maximum XOR value out of all possible strong pairs in the array nums.

Note that you can pick the same integer twice to form a pair.
"""

class TrieNode:
    def __init__(self):
        self.children={}
        self.val=0
        
class Trie:
    def __init__(self):
        self.root=TrieNode()
        
    def add(self,num,freq):
        node=self.root
        for i in range(20,-1,-1):
            bit=(num>>i)&1
            if bit not in node.children:
                node.children[bit]=TrieNode()
            node=node.children[bit]
            node.val+=freq
            
    def getMax(self,x):
        node,res=self.root,0
        for i in range(20,-1,-1):
            bit=(x>>i)&1
            if bit^1 in node.children and node.children[bit^1].val:
                node=node.children[bit^1]
                res+=1<<i
            elif bit^0 in node.children and node.children[bit^0].val:
                node=node.children[bit^0]
            else:
                return -math.inf
        return res

class Solution:
    def maximumStrongPairXor(self, nums: List[int]) -> int:
        res=-math.inf
        nums.sort()
        l=0
        t=Trie()
        for r in range(len(nums)):
            t.add(nums[r],1)
            while nums[l]*2<nums[r]:
                t.add(nums[l],-1)
                l+=1
            res=max(res,t.getMax(nums[r]))
        return res


"""
2953. Count Complete Substrings

You are given a string word and an integer k.

A substring s of word is complete if:

Each character in s occurs exactly k times.
The difference between two adjacent characters is at most 2. That is, for any two adjacent characters c1 and c2 in s, the absolute difference in their positions in the alphabet is at most 2.
Return the number of complete substrings of word.

A substring is a non-empty contiguous sequence of characters in a string.
"""

class Solution:
    def countCompleteSubstrings(self, word: str, k: int) -> int:
        def f(x):
            cnt=Counter()
            found=left=res=chars=0
            for idx,i in enumerate(word):
                if idx>0 and abs(ord(word[idx])-ord(word[idx-1]))>2:
                    cnt=Counter()
                    found=chars=0
                    left=idx
                cnt[i]+=1
                if cnt[i]==k:found+=1
                chars+=1
                if found==x:
                    res+=1
                if chars>=k*x:
                    cnt[word[left]]-=1
                    if cnt[word[left]]==k-1:found-=1
                    left+=1
                    chars-=1
            return res
        
        return sum(f(i) for i in range(1,27))


"""
3008. Find Beautiful Indices in the Given Array II

You are given a 0-indexed string s, a string a, a string b, and an integer k.

An index i is beautiful if:

0 <= i <= s.length - a.length
s[i..(i + a.length - 1)] == a
There exists an index j such that:
0 <= j <= s.length - b.length
s[j..(j + b.length - 1)] == b
|j - i| <= k
Return the array that contains beautiful indices in sorted order from smallest to largest.
"""

class Solution:
    def beautifulIndices(self, s: str, a: str, b: str, k: int) -> List[int]:
        def f(x):
            cur,mod=0,10**9+9
            for i in x:
                cur=(cur*31+ord(i)-97)%mod
            return cur
        
        def y(x,s,tar):
            cur,mod=0,10**9+9
            res=[]
            for idx,i in enumerate(x):
                cur=(cur*31+ord(i)-97)%mod
                if idx>=len(s)-1:
                    if cur==tar:res+=[idx-len(s)+1]
                    cur=(cur-(ord(x[idx-len(s)+1])-97)*pow(31,len(s)-1,mod))%mod
            return res
                
        av,bv,p=f(a),f(b),0
        A,B,res=y(s,a,av),y(s,b,bv),[]
        for idx in A:
            while p<len(B) and B[p]<idx-k:
                p+=1
            if p<len(B) and abs(B[p]-idx)<=k:
                res+=[idx]
        return res


"""
3013. Divide an Array Into Subarrays With Minimum Cost II

You are given a 0-indexed array of integers nums of length n, and two positive integers k and dist.

The cost of an array is the value of its first element. For example, the cost of [1,2,3] is 1 while the cost of [3,4,1] is 3.

You need to divide nums into k disjoint contiguous subarrays, such that the difference between the starting index of the second subarray and the starting index of the kth subarray should be less than or equal to dist. In other words, if you divide nums into the subarrays nums[0..(i1 - 1)], nums[i1..(i2 - 1)], ..., nums[ik-1..(n - 1)], then ik-1 - i1 <= dist.

Return the minimum possible sum of the cost of these subarrays.
"""


class Solution:
    def minimumCost(self, nums: List[int], k: int, dist: int) -> int:
        A=SortedList()
        res,tot=math.inf,0
        for i in range(1,len(nums)):
            if i>1+dist:
                idx=bisect_left(A,nums[i-dist-1])
                if idx>=k-1:
                    A.pop(idx)
                else:
                    tot-=A.pop(idx)
                    if len(A)>=k-1:tot+=A[k-2]
            if len(A)<k-1:
                tot+=nums[i]
            else:
                idx=bisect_left(A,nums[i])
                if idx<=k-2:
                    tot+=nums[i]
                    tot-=A[k-2]
            A.add(nums[i])
            if len(A)>=k-1:
                res=min(res,nums[0]+tot)
        return res

        
"""
3041. Maximize Consecutive Elements in an Array After Modification

You are given a 0-indexed array nums consisting of positive integers.

Initially, you can increase the value of any element in the array by at most 1.

After that, you need to select one or more elements from the final array such that those elements are consecutive when sorted in increasing order. For example, the elements [3, 4, 5] are consecutive while [3, 4, 6] and [1, 1, 2, 3] are not.
Return the maximum number of elements that you can select.
"""

class Solution:
    def maxSelectedElements(self, nums: List[int]) -> int:
        nums.sort()
    
        @cache
        def f(idx,inc):
            if idx==len(nums):
                return 0
            cur=nums[idx]+inc
            x=bisect_left(nums,cur,idx+1)
            y=bisect_left(nums,cur+1,idx+1)
            res=1
            if x<len(nums) and nums[x]==cur:res=max(res,1+f(x,1))
            if y<len(nums) and nums[y]==cur+1:res=max(res,1+f(y,0))
            return res
        
        return max(max(f(i,1),f(i,0)) for i in range(len(nums)))


"""
3045. Count Prefix and Suffix Pairs II

You are given a 0-indexed string array words.

Let's define a boolean function isPrefixAndSuffix that takes two strings, str1 and str2:

isPrefixAndSuffix(str1, str2) returns true if str1 is both a prefix and a suffix of str2, and false otherwise.
For example, isPrefixAndSuffix("aba", "ababa") is true because "aba" is a prefix of "ababa" and also a suffix, but isPrefixAndSuffix("abc", "abcd") is false.

Return an integer denoting the number of index pairs (i, j) such that i < j, and isPrefixAndSuffix(words[i], words[j]) is true.
"""

class TrieNode:
    def __init__(self):
        self.children={}
        self.freq=0
        self.idx=-1
        
class Trie:
    def __init__(self):
        self.root=TrieNode()
        
    def add(self,word,idx):
        node=self.root
        for w in word:
            if w not in node.children:
                node.children[w]=TrieNode()
            node=node.children[w]
        node.freq+=1
        node.idx=idx
        
    def get(self,word,seen):
        res,node=0,self.root
        for w in word:
            if w in node.children:
                node=node.children[w]
                res+=node.freq*(node.idx in seen)*(node.idx!=-1)
                seen.add(node.idx)
            else:break
        return res


class Solution:
    def countPrefixSuffixPairs(self, words: List[str]) -> int:
        pref,suf,res=Trie(),Trie(),0
        for idx,w in enumerate(words):
            seen=set()
            res+=pref.get(w,seen)+suf.get(w[::-1],seen)
            pref.add(w,idx)
            suf.add(w[::-1],idx)
        return res


            
"""
3187. Peaks in Array

A peak in an array arr is an element that is greater than its previous and next element in arr.

You are given an integer array nums and a 2D integer array queries.

You have to process queries of two types:

queries[i] = [1, li, ri], determine the count of peak elements in the subarray nums[li..ri].
queries[i] = [2, indexi, vali], change nums[indexi] to vali.
Return an array answer containing the results of the queries of the first type in order.
Notes:

The first and the last element of an array or a subarray cannot be a peak.
"""

class Solution:
    def countOfPeaks(self, nums: List[int], queries: List[List[int]]) -> List[int]:
        n=len(nums)
        tree=[0]*(n+1)
        
        def check(idx):
            return idx>0 and idx<n-1 and nums[idx-1]<nums[idx]>nums[idx+1]
    
        def add(idx,val):
            idx+=1
            while idx<len(tree):
                tree[idx]+=val
                idx+=idx&(-idx)
            
        def getVal(idx):
            idx,res=idx+1,0
            while idx>0:
                res+=tree[idx]
                idx-=idx&(-idx)
            return res
    
        for i in range(1,n):
            if check(i):
                add(i,1)
    
        res=[]
        for a,b,c in queries:
            if a==1:
                left=check(b)
                right=check(c)
                res+=[getVal(c)-(getVal(b-1) if b>0 else 0)-left-right if b!=c else 0]
            else:
                prev=[(b-1,check(b-1)),(b,check(b)),(b+1,check(b+1))]
                nums[b]=c
                cur=[(b-1,check(b-1)),(b,check(b)),(b+1,check(b+1))]
                for a,b in zip(prev,cur):
                    idx=b[0]
                    change=b[1]-a[1]
                    if idx>0:add(idx,change)
                    
        return res
