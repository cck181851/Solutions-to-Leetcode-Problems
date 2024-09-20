from sortedcontainers import SortedList
import itertools, functools, bisect 

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
