# https://leetcode.com/problems/maximum-elegance-of-a-k-length-subsequence/
class Solution:
    def findMaximumElegance(self, items: List[List[int]], k: int) -> int:
        items.sort(reverse=True)
        profit = res = 0
        cnt = Counter()
        q = list()
        for idx,[p,c] in enumerate(items):
            if idx<k:
                cnt[c] += 1
                profit += p
                heappush(q,[p,c])
            elif c not in cnt:
                while q and cnt[q[0][1]] == 1:
                    heappop(q)
                if not q:
                    continue
                pp,pc = heappop(q)
                profit += p-pp
                cnt[pc] -= 1
                cnt[c] += 1
            res = max(res,profit + len(cnt)**2)    
                 
        return res
