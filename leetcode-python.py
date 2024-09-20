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
