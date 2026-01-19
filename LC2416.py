# https://leetcode.com/problems/sum-of-prefix-scores-of-strings/
mod=10**18+7
class Solution:
    def sumPrefixScores(self, words: List[str]) -> List[int]:
        cnt=Counter()
        res=list()
        for word in words:
            cur=0
            for w in word:
                cur=(cur*26+ord(w)-96)%mod
                cnt[cur]+=1
        for word in words:
            cur=tmp=0
            for w in word:  
                cur=(cur*26+ord(w)-96)%mod
                tmp+=cnt[cur]
            res.append(tmp)
        return res
