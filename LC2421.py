# https://leetcode.com/problems/number-of-good-paths/description/
class Solution:
    def numberOfGoodPaths(self, vals: List[int], edges: List[List[int]]) -> int:
        rank=[0 for _ in range(len(vals))]
        par=[i for i in range(len(vals))]

        def find(x):
            while x!=par[x]:x=par[x]
            return par[x]

        def union(x,y):
            px,py=find(x),find(y)
            if px==py:return
            if rank[py]>rank[px]:px,py=py,px
            rank[px]+=rank[py]
            par[py]=px

        graph=defaultdict(list)
        for a,b in edges:
            graph[a].append(b)
            graph[b].append(a)

        d=defaultdict(list)
        for idx,val in enumerate(vals):
            d[val].append(idx)

        res=0
        for k,v in sorted(d.items()):
            for val in v:
                rank[find(val)]+=1
            for val in v:
                for n in graph[val]:
                    if rank[find(n)]>0:
                        union(val,n)
            tmp=defaultdict(list)
            for val in v:
                tmp[find(val)].append(val)             
            for group in tmp.values():
                res+=len(group)*(len(group)-1)//2

        return res+len(vals)    
