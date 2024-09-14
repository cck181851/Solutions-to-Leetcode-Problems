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
                
            
