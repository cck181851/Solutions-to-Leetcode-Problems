/*
3. Longest Substring Without Repeating Characters
Given a string s, find the length of the longest substring without repeating characters.
*/

class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        int arr[130],left=0,res=0;
        for(int i=0;i<s.length();res=max(res,i-left+1),i++){
            arr[s[i]]++;
            while(arr[s[i]]>1) arr[s[left++]]--;
        }
        return res;
    }
};

/*
9. Palindrome Number
Given an integer x, return true if x is a palindrome, and false otherwise.
*/
  
class Solution {
public:
    bool isPalindrome(int x) {
        string a=to_string(x),b=a;
        reverse(b.begin(),b.end());
        return a==b;
    }
};

/*
85. Maximal Rectangle
Given a rows x cols binary matrix filled with 0's and 1's, find the largest rectangle containing only 1's and return its area.
*/

class Solution {
public:
    int maximalRectangle(vector<vector<char>>& matrix) {
        auto A=f(matrix);
        int res=0;
        for(auto& row:A){
            row.push_back(0);
            vector<int> stack={-1};
            for(int i=0;i<row.size();i++){
                while(stack.back()!=-1 && row[stack.back()]>=row[i]){
                    int val=row[stack.back()];
                    stack.pop_back();
                    res=max(res,(i-stack.back()-1)*val);
                }
                res=max(res,(i-stack.back()-1)*row[i]);
                stack.push_back(i);
            }
        }
        return res;
    }
    vector<vector<int>> f(auto& A){
        vector<vector<int>> res(A.size(),vector<int>(A[0].size()));
        for(int i=0;i<A.size();i++){
            for(int j=0;j<A[0].size();j++){
                res[i][j]=A[i][j]-'0';
                if(i>0 && res[i][j]){
                    res[i][j]+=res[i-1][j];
                }
            }
        }
        return res;
    } 
};

/*
147. Insertion Sort List
Given the head of a singly linked list, sort the list using insertion sort, and return the sorted list's head.

The steps of the insertion sort algorithm:

Insertion sort iterates, consuming one input element each repetition and growing a sorted output list.
At each iteration, insertion sort removes one element from the input data, finds the location it belongs within the sorted list and inserts it there.
It repeats until no input elements remain.
The following is a graphical example of the insertion sort algorithm. The partially sorted list (black) initially contains only the first element in the list. One element (red) is removed from the input data and inserted in-place into the sorted list with each iteration.
*/

/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode() : val(0), next(nullptr) {}
 *     ListNode(int x) : val(x), next(nullptr) {}
 *     ListNode(int x, ListNode *next) : val(x), next(next) {}
 * };
 */

class Solution {
public:
    ListNode* insertionSortList(ListNode* head) {
        ListNode* dummy=new ListNode(-1);
        while(head!=nullptr){
            ListNode* rem=head->next,*beg=dummy,*end=dummy->next;
            while(end!=nullptr){
                if(end->val > head->val) break;
                beg=end;
                end=end->next;
            }
            beg->next=head;
            head->next=end;
            head=rem;
        }
        return dummy->next;
    }
};

/*
322. Coin Change
You are given an integer array coins representing coins of different denominations and an integer amount representing a total amount of money.

Return the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return -1.

You may assume that you have an infinite number of each kind of coin.
*/

class Solution {
public:
    int coinChange(vector<int>& coins, int amount) {
        int memo[12][10001],res;
        memset(memo,-1,sizeof(memo));
        sort(coins.begin(),coins.end(),[&](int x,int y){return x>y;});
        
        function<int(int,int)> f=[&](int idx,int rem){
            if(rem<=0 || idx==coins.size()){
                return rem==0 ? 0:10001;
            }
            if(memo[idx][rem]==-1){
                int res=min(f(idx+1,rem),1+f(idx,rem-coins[idx]));
                memo[idx][rem]=res;
            }
            return memo[idx][rem];
        };
        
        res=f(0,amount);
        return res>10000 ? -1:res;
    }
};

/*
410. Split Array Largest Sum
Given an integer array nums and an integer k, split nums into k non-empty subarrays such that the largest sum of any subarray is minimized.

Return the minimized largest sum of the split.

A subarray is a contiguous part of the array.
*/

class Solution {
public:
    int splitArray(vector<int>& nums, int k) {
        int left=*max_element(nums.begin(),nums.end()),right=1e9;
        while(left<right){
            int mid=(left+right)/2;
            if(f(mid,nums,k)) right=mid;
            else left=mid+1;
        }
        return left;
    }
    bool f(int x,vector<int>& nums,int k){
        int parts=0,tot=0;
        for(int num:nums){
            if((tot+num)<=x){
                tot+=num;
            }
            else{
                tot=num;
                ++parts;
            }
        }
        return (parts+1)<=k;
    }
};

/*
424. Longest Repeating Character Replacement
You are given a string s and an integer k. You can choose any character of the string and change it to any other uppercase English character. You can perform this operation at most k times.

Return the length of the longest substring containing the same letter you can get after performing the above operations.
*/

class Solution {
public:
    int characterReplacement(string s, int k) {
        int res=0;
        for(char ch:unordered_set<char>(s.begin(),s.end())){
            res=max(res,f(ch,k,s));
        }
        return res;
    }
    
    int f(char i,int k,string& s){
        int left,res,cur;
        for(int j=0;j<s.length();j++){
            cur+=(s[j]==i ? 1:0);
            while((j-left+1-cur)>k){ 
                cur-=(s[left++]==i ? 1:0);
            }
            res=max(res,j-left+1);
        }
        return res;
    }
};

/*
632. Smallest Range Covering Elements from K Lists

You have k lists of sorted integers in non-decreasing order. Find the smallest range that includes at least one number from each of the k lists.

We define the range [a, b] is smaller than range [c, d] if b - a < d - c or a < c if b - a == d - c.
*/

class Solution {
public:
    vector<int> smallestRange(vector<vector<int>>& nums) {
        vector<vector<int>> A;
        for(int i=0;i<nums.size();i++){
            for(int j:nums[i]){
                A.push_back({j,i});
            }
        }
        sort(A.begin(),A.end());
        vector<int> cnt(nums.size(),0),res{0,(int)1e6};
        for(int l=0,r=0,found=0;r<A.size();r++){
            if(++cnt[A[r][1]]==1){
                ++found;
            }
            while(cnt[A[l][1]]>1){
                --cnt[A[l++][1]];
            }
            if(found==nums.size() && ((res[1]-res[0])>(A[r][0]-A[l][0]) || 
                (A[r][0]-A[l][0])==(res[1]-res[0]) && res[0]>A[l][0])){
                res=vector<int>{A[l][0],A[r][0]}; 
            }
        }
        return res;
    }
};


/*
907. Sum of Subarray Minimums

Given an array of integers arr, find the sum of min(b), where b ranges over every (contiguous) subarray of arr. Since the answer may be large, return the answer modulo 109 + 7.
*/

class Solution {
public:
    vector<int> smallestRange(vector<vector<int>>& nums) {
        vector<vector<int>> A;
        for(int i=0;i<nums.size();i++){
            for(int j:nums[i]){
                A.push_back({j,i});
            }
        }
        sort(A.begin(),A.end());
        vector<int> cnt(nums.size(),0),res{0,(int)1e6};
        for(int l=0,r=0,found=0;r<A.size();r++){
            if(++cnt[A[r][1]]==1){
                ++found;
            }
            while(cnt[A[l][1]]>1){
                --cnt[A[l++][1]];
            }
            if(found==nums.size() && ((res[1]-res[0])>(A[r][0]-A[l][0]) || 
                (A[r][0]-A[l][0])==(res[1]-res[0]) && res[0]>A[l][0])){
                res=vector<int>{A[l][0],A[r][0]}; 
            }
        }
        return res;
    }
};

/*

1234. Replace the Substring for Balanced String

You are given a string s of length n containing only four kinds of characters: 'Q', 'W', 'E', and 'R'.

A string is said to be balanced if each of its characters appears n / 4 times where n is the length of the string.

Return the minimum length of the substring that can be replaced with any other string of the same length to make s balanced. If s is already balanced, return 0.

*/

class Solution {
public:
    int balancedString(string s) {
        unordered_map<char,int> cnt;
        int width=s.length(),tar=s.length()/4,left=0;
        for(char& c:s){
            cnt[c]++;
        }
        for(int i=0;i<s.length();i++){
            --cnt[s[i]];
            while(left<=i && cnt[s[left]]<tar){
                cnt[s[left++]]++;
            }
            if(cnt['Q']<=tar && cnt['W']<=tar && cnt['E']<=tar && cnt['R']<=tar) {
                width=min(width,i-left+1);
            }
        }
        return width;
    }
};
/*

1458. Max Dot Product of Two Subsequences

Given two arrays nums1 and nums2.

Return the maximum dot product between non-empty subsequences of nums1 and nums2 with the same length.

A subsequence of a array is a new array which is formed from the original array by deleting some (can be none) of the characters without disturbing the relative positions of the remaining characters. (ie, [2,3,5] is a subsequence of [1,2,3,4,5] while [1,5,3] is not).
*/

class Solution {
public:
    int maxDotProduct(vector<int>& nums1, vector<int>& nums2) {
        long long memo[501][501][2];
        memset(memo,-1,sizeof(memo));
        
        function<long long(int,int,int)> f=[&](int i,int j,int k){
            if(i==nums1.size() || j==nums2.size()){
                return (long long)(k==0 ? INT_MIN:0);
            }
            if(memo[i][j][k]==-1){
                memo[i][j][k]=max(f(i+1,j,k),max(f(i,j+1,k),nums1[i]*nums2[j]+f(i+1,j+1,1)));
            }
            return memo[i][j][k];
        };
        
        return f(0,0,0);
    }
};

/*

1462. Course Schedule IV

There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course ai first if you want to take course bi.

For example, the pair [0, 1] indicates that you have to take course 0 before you can take course 1.
Prerequisites can also be indirect. If course a is a prerequisite of course b, and course b is a prerequisite of course c, then course a is a prerequisite of course c.

You are also given an array queries where queries[j] = [uj, vj]. For the jth query, you should answer whether course uj is a prerequisite of course vj or not.

Return a boolean array answer, where answer[j] is the answer to the jth query.

*/

class Solution {
public:
    vector<bool> checkIfPrerequisite(int numCourses, vector<vector<int>>& prerequisites, vector<vector<int>>& queries) {
        vector<vector<int>> tree(numCourses,vector<int>());
        vector<unordered_set<int>> res(numCourses,unordered_set<int>());
        vector<int> visited(101,0);
        
        for(auto& p:prerequisites){
            tree[p[0]].push_back(p[1]);
        }
    
        function<unordered_set<int>(int)> f=[&](int node){
            if(++visited[node]>1){
                return res[node];
            }
            unordered_set<int> tmp={node};
            for(int child:tree[node]){
                auto anc=f(child);
                tmp.insert(anc.begin(),anc.end());
            }
            for_each(tmp.begin(),tmp.end(),[&](int i){res[node].insert(i);});
            return tmp;
        };
        
        for(int i=0;i<numCourses;i++){
            if(visited[i]==0) f(i);
        }
        
        vector<bool> ans;
        transform(queries.begin(),queries.end(),back_inserter(ans),[&](auto& a){
            return res[a[0]].count(a[1])>0;
        });
        return ans;
    }
};

/*

1609. Even Odd Tree

A binary tree is named Even-Odd if it meets the following conditions:

The root of the binary tree is at level index 0, its children are at level index 1, their children are at level index 2, etc.
For every even-indexed level, all nodes at the level have odd integer values in strictly increasing order (from left to right).
For every odd-indexed level, all nodes at the level have even integer values in strictly decreasing order (from left to right).
Given the root of a binary tree, return true if the binary tree is Even-Odd, otherwise return false.
*/

/**
 * Definition for a binary tree node.
 * struct TreeNode {
 *     int val;
 *     TreeNode *left;
 *     TreeNode *right;
 *     TreeNode() : val(0), left(nullptr), right(nullptr) {}
 *     TreeNode(int x) : val(x), left(nullptr), right(nullptr) {}
 *     TreeNode(int x, TreeNode *left, TreeNode *right) : val(x), left(left), right(right) {}
 * };
 */
class Solution {
public:
    bool isEvenOddTree(TreeNode* root) {
        deque<TreeNode*> q={root};
        int level=0;
        while(!q.empty()){
            int prev=level%2==0 ? -1:1e8,size=q.size();
            for(int i=0;i<size;i++){
                TreeNode* node=q.front();q.pop_front();
                if(!(node==nullptr)){
                    if(level%2 == node->val%2) return false;
                    int dif=node->val-prev;
                    if(level%2==0 && dif<=0 || level%2==1 && dif>=0) return false;
                    prev=node->val;
                    q.push_back(node->left);q.push_back(node->right);
                } 
            }
            ++level;
        }
        return true;
    }
};
/*

1671. Minimum Number of Removals to Make Mountain Array

You may recall that an array arr is a mountain array if and only if:

arr.length >= 3
There exists some index i (0-indexed) with 0 < i < arr.length - 1 such that:
arr[0] < arr[1] < ... < arr[i - 1] < arr[i]
arr[i] > arr[i + 1] > ... > arr[arr.length - 1]
Given an integer array nums​​​, return the minimum number of elements to remove to make nums​​​ a mountain array.

*/

class Solution {
public:
    int minimumMountainRemovals(vector<int>& nums) {
        vector<int> A=f(nums);
        reverse(nums.begin(),nums.end());
        vector<int> B=f(nums);
        int res=0;
        for(int i=0;i<A.size();i++){
            if(A[i]>1 && B[B.size()-i-1]>1){ 
                res=max(res,A[i]+B[B.size()-i-1]);
            }
        }
        return A.size()-res+1;
    }
    vector<int> f(vector<int>& A){
        vector<int> res,B;
        for(int i:A){
            if(B.empty() || i>B.back()){
                B.push_back(i);
                res.push_back(B.size());
            }
            else{
                int idx=lower_bound(B.begin(),B.end(),i)-B.begin();
                B[idx]=i;
                res.push_back(idx+1);
            }
        }
        return res;
    }
};

/*

1685. Sum of Absolute Differences in a Sorted Array

You are given an integer array nums sorted in non-decreasing order.

Build and return an integer array result with the same length as nums such that result[i] is equal to the summation of absolute differences between nums[i] and all the other elements in the array.

In other words, result[i] is equal to sum(|nums[i]-nums[j]|) where 0 <= j < nums.length and j != i (0-indexed).

*/

class Solution {
public:
    vector<int> getSumAbsoluteDifferences(vector<int>& nums) {
        int pref=0,suf=accumulate(nums.begin(),nums.end(),0);
        vector<int> res;
        for(int i=0;i<nums.size();i++){
            suf-=nums[i];
            res.push_back(i*nums[i]-pref+suf-(nums.size()-i-1)*nums[i]);
            pref+=nums[i];
        }
        return res;
    }
};

/*

1712. Ways to Split Array Into Three Subarrays

A split of an integer array is good if:

The array is split into three non-empty contiguous subarrays - named left, mid, right respectively from left to right.
The sum of the elements in left is less than or equal to the sum of the elements in mid, and the sum of the elements in mid is less than or equal to the sum of the elements in right.
Given nums, an array of non-negative integers, return the number of good ways to split nums. As the number may be too large, return it modulo 109 + 7.

*/

class Solution {
public:
    int waysToSplit(vector<int>& nums) {
        int tot=nums[0],res=0,mod=1e9+7,n=nums.size();
        for(int i=1;i<nums.size();i++){
            tot+=nums[i];
            nums[i]+=nums[i-1];
        }
        for(int i=0;i<nums.size();i++){
            auto f1=lower_bound(nums.begin()+i+1,nums.end(),nums[i]*2)-nums.begin();
            auto f2=upper_bound(nums.begin()+i+1,nums.begin()+n-1,(tot+nums[i])/2)-nums.begin();
            res+=f2>f1 ? f2-f1:0;
            res%=mod;
        }
        return res;
    }
};

/*

1743. Restore the Array From Adjacent Pairs

There is an integer array nums that consists of n unique elements, but you have forgotten it. However, you do remember every pair of adjacent elements in nums.

You are given a 2D integer array adjacentPairs of size n - 1 where each adjacentPairs[i] = [ui, vi] indicates that the elements ui and vi are adjacent in nums.

It is guaranteed that every adjacent pair of elements nums[i] and nums[i+1] will exist in adjacentPairs, either as [nums[i], nums[i+1]] or [nums[i+1], nums[i]]. The pairs can appear in any order.

Return the original array nums. If there are multiple solutions, return any of them.

*/

class Solution {
public:
    vector<int> restoreArray(vector<vector<int>>& A) {
        unordered_map<int,vector<int>> B;
        vector<int> res;
        
        for(auto& ab:A){
            B[ab[0]].push_back(ab[1]);
            B[ab[1]].push_back(ab[0]);
        }
        
        for(auto& b:B){
            if(b.second.size()==1){
                res.push_back(b.first);
                break;
            }
        }
        while(res.size()<A.size()+1){
            int cur=res.back(),nxt=B[cur].back();
            B[cur].pop_back();
            B[nxt].erase(find(B[nxt].begin(),B[nxt].end(),cur));
            res.push_back(nxt);
        }
        return res;
    }
};

/*

1751. Maximum Number of Events That Can Be Attended II

You are given an array of events where events[i] = [startDayi, endDayi, valuei]. The ith event starts at startDayi and ends at endDayi, and if you attend this event, you will receive a value of valuei. You are also given an integer k which represents the maximum number of events you can attend.

You can only attend one event at a time. If you choose to attend an event, you must attend the entire event. Note that the end day is inclusive: that is, you cannot attend two events where one of them starts and the other ends on the same day.

Return the maximum sum of values that you can receive by attending events.

*/

class Solution {
public:
    int maxValue(vector<vector<int>>& events, int k) {
        sort(events.begin(),events.end());
        vector<vector<int>> memo(events.size()+1,vector<int>(k+1,-1));
        return f(0,k,events,memo);
        
    }
    int f(int idx,int rem,vector<vector<int>>& events,auto& memo){
        if(idx==events.size()){
            return 0;
        }
        if(memo[idx][rem]==-1){
            auto i = upper_bound(begin(events) + idx, end(events), events[idx][1], 
            [](int t, const vector<int> &v) {return v[0] > t;}) - begin(events);
            int res=f(idx+1,rem,events,memo);
            if(rem>0) res=max(res,f(i,rem-1,events,memo)+events[idx][2]);
            memo[idx][rem]=res;
        }
        return memo[idx][rem];
    } 
};

/*

1755. Closest Subsequence Sum

You are given an integer array nums and an integer goal.

You want to choose a subsequence of nums such that the sum of its elements is the closest possible to goal. That is, if the sum of the subsequence's elements is sum, then you want to minimize the absolute difference abs(sum - goal).

Return the minimum possible value of abs(sum - goal).

Note that a subsequence of an array is an array formed by removing some elements (possibly all or none) of the original array.

*/

class Solution {
public:
    int minAbsDifference(vector<int>& nums, int goal) {
        int n=nums.size(),res=INT_MAX;
        vector<int> B1,B2,A1(nums.begin(),nums.begin()+n/2),A2(nums.begin()+n/2,nums.end());
        f(0,0,A1,B1);
        f(0,0,A2,B2);
        sort(B1.begin(),B1.end());
        sort(B2.begin(),B2.end());
        for(int j:B1){
            int idx=lower_bound(B2.begin(),B2.end(),goal-j)-B2.begin();
            if(idx<B2.size()) res=min(res,abs(goal-B2[idx]-j));
            if(idx>0) res=min(res,abs(goal-B2[idx-1]-j));
        }
        return res;
        
    }
    void f(int idx,int cur,vector<int>& A,vector<int>& B){
        if(idx==A.size()){
            B.push_back(cur);
            return;
        }
        f(idx+1,cur+A[idx],A,B);
        f(idx+1,cur,A,B);
    }
};

/*

1766. Tree of Coprimes

There is a tree (i.e., a connected, undirected graph that has no cycles) consisting of n nodes numbered from 0 to n - 1 and exactly n - 1 edges. Each node has a value associated with it, and the root of the tree is node 0.

To represent this tree, you are given an integer array nums and a 2D array edges. Each nums[i] represents the ith node's value, and each edges[j] = [uj, vj] represents an edge between nodes uj and vj in the tree.

Two values x and y are coprime if gcd(x, y) == 1 where gcd(x, y) is the greatest common divisor of x and y.

An ancestor of a node i is any other node on the shortest path from node i to the root. A node is not considered an ancestor of itself.

Return an array ans of size n, where ans[i] is the closest ancestor to node i such that nums[i] and nums[ans[i]] are coprime, or -1 if there is no such ancestor.

*/

class Solution {
public:
    vector<int> getCoprimes(vector<int>& nums, vector<vector<int>>& edges) {
        vector<vector<int>> A(51,vector<int>());
        vector<vector<int>> tree(nums.size(),vector<int>());
        vector<vector<pair<int,int>>> pars(51,vector<pair<int,int>>());
        
        for(int i=0;i<=50;i++){
            for(int j=0;j<=50;j++){
                if(gcd(i,j)==1) A[i].push_back(j);
            }
        }
        
        for(auto& n:edges){
            tree[n[0]].push_back(n[1]);
            tree[n[1]].push_back(n[0]);
        }
        
        vector<int> res(nums.size(),-1);
        function<void(int,int,int)> f=[&](int node,int level,int par){
            int val=nums[node],cur_res=-1;
            for(int a:A[val]){
                if(!pars[a].empty() && pars[a].back().first>cur_res){
                    cur_res=pars[a].back().first;
                    res[node]=pars[a].back().second;
                }
            }
            pars[val].push_back({level,node});
            for(int child:tree[node]){
                if(child==par) continue;
                f(child,level+1,node);
            }
            pars[val].pop_back();
        };
        
        f(0,0,-1);
        return res;
    }
};

/*

1771. Maximize Palindrome Length From Subsequences

You are given two strings, word1 and word2. You want to construct a string in the following manner:

Choose some non-empty subsequence subsequence1 from word1.
Choose some non-empty subsequence subsequence2 from word2.
Concatenate the subsequences: subsequence1 + subsequence2, to make the string.
Return the length of the longest palindrome that can be constructed in the described manner. If no palindromes can be constructed, return 0.

A subsequence of a string s is a string that can be made by deleting some (possibly none) characters from s without changing the order of the remaining characters.

A palindrome is a string that reads the same forward as well as backward.

*/

class Solution {
public:
    int memo[2][1000][1000],memo2[1000][1000][2];
    int longestPalindrome(string w1, string w2) {
        memset(memo,-1,sizeof(memo));
        memset(memo2,-1,sizeof(memo2));
        return pal(w1,w2,0,w2.length()-1,0);
    }
    int f(string& w1,string& w2,int i,int left,int right){
        string& w=(i==0 ? w1:w2);
        if (left>right){
            return 0;
        }
        int* A=&memo[i][left][right];
        if(*A==-1 && w[left]==w[right]){
            *A=f(w1,w2,i,left+1,right-1)+(left==right ? 1:2);
        }
        if(*A==-1 && w[left]!=w[right]){
            *A=max(f(w1,w2,i,left+1,right),f(w1,w2,i,left,right-1));
        }
        return *A;
    }
    int pal(string& w1,string& w2,int i,int j,int k){
        if(i==w1.length() || j==-1){
            return k==1 ? f(w1,w2,0,i,w1.length()-1)+f(w1,w2,1,0,j):0;
        }
        int* A=&memo2[i][j][k];
        if(*A==-1){
            if(w1[i]==w2[j]){
                *A=2+pal(w1,w2,i+1,j-1,1);
            } 
            else{
                *A=max(pal(w1,w2,i+1,j,k),pal(w1,w2,i,j-1,k));
            }
        }
        return *A;
    }
};

/*
2009. Minimum Number of Operations to Make Array Continuous

You are given an integer array nums. In one operation, you can replace any element in nums with any integer.

nums is considered continuous if both of the following conditions are fulfilled:

All elements in nums are unique.
The difference between the maximum element and the minimum element in nums equals nums.length - 1.
For example, nums = [4, 2, 5, 3] is continuous, but nums = [1, 2, 3, 5, 6] is not continuous.

Return the minimum number of operations to make nums continuous.

*/

class Solution {
public:
    int minOperations(vector<int>& nums) {
        int init=nums.size(),match=0;
        sort(nums.begin(),nums.end());
        nums.erase(unique(nums.begin(),nums.end()),nums.end());
        for(int i=0;i<nums.size();i++){
            int idx=lower_bound(nums.begin(),nums.end(),nums[i]+init)-nums.begin();
            match=max(match,idx-i);
        }
        return init-match;
    }
};

/*
2030. Smallest K-Length Subsequence With Occurrences of a Letter

You are given a string s, an integer k, a letter letter, and an integer repetition.

Return the lexicographically smallest subsequence of s of length k that has the letter letter appear at least repetition times. The test cases are generated so that the letter appears in s at least repetition times.

A subsequence is a string that can be derived from another string by deleting some or no characters without changing the order of the remaining characters.

A string a is lexicographically smaller than a string b if in the first position where a and b differ, string a has a letter that appears earlier in the alphabet than the corresponding letter in b.
*/

class Solution {
public:
    string smallestSubsequence(string s, int k, char letter, int r) {
        vector<int> A;
        int rem=count(s.begin(),s.end(),letter),cur=0;
        auto f=[&](int i){
            return (A.size()+s.length()-i-1)>=k && 
            (rem+cur-(A.back()==letter ? 1:0))>=r && s[i]<A.back();
        };
        for(int i=0;i<s.length();i++){
            while(!A.empty() && f(i)){
                cur-=letter==A.back() ? 1:0;
                A.pop_back();
            }
            cur+=letter==s[i] ? 1:0;
            rem-=letter==s[i] ? 1:0;
            A.push_back(s[i]);
        }
        string res="";
        int take=k-r;
        for(int i:A){
            if(res.length()==k) break;
            if(i==letter || take>0){
                take-=i==letter ? 0:1;
                res+=i;
            }
        }
        return res;
    }
};

/*

2050. Parallel Courses III

You are given an integer n, which indicates that there are n courses labeled from 1 to n. You are also given a 2D integer array relations where relations[j] = [prevCoursej, nextCoursej] denotes that course prevCoursej has to be completed before course nextCoursej (prerequisite relationship). Furthermore, you are given a 0-indexed integer array time where time[i] denotes how many months it takes to complete the (i+1)th course.

You must find the minimum number of months needed to complete all the courses following these rules:

You may start taking a course at any time if the prerequisites are met.
Any number of courses can be taken at the same time.
Return the minimum number of months needed to complete all the courses.

Note: The test cases are generated such that it is possible to complete every course (i.e., the graph is a directed acyclic graph).

*/

class Solution {
public:
    int minimumTime(int n, vector<vector<int>>& relations, vector<int>& times) {
        vector<vector<int>> preq(n+1,vector<int>());
        vector<int> rank(n+1,0);
        for(auto& a:relations){
            preq[a[0]].push_back(a[1]);
            ++rank[a[1]];
        }
        priority_queue<array<int,2>,vector<array<int,2>>,greater<>> q;
        for(int i=1;i<=n;i++){
            if(rank[i]==0) q.push({times[i-1],i});
        }
        int taken=0,time=0;
        while(taken<n){
            time=q.top()[0];
            while(!q.empty() && q.top()[0]==time){
                int course=q.top()[1];
                q.pop();
                ++taken;
                for(int m:preq[course]){
                    --rank[m];
                    if(rank[m]==0){
                        q.push({times[m-1]+time,m});
                    }
                }
            }
        }
        return time;
    }
};

/*

2163. Minimum Difference in Sums After Removal of Elements

You are given a 0-indexed integer array nums consisting of 3 * n elements.

You are allowed to remove any subsequence of elements of size exactly n from nums. The remaining 2 * n elements will be divided into two equal parts:

The first n elements belonging to the first part and their sum is sumfirst.
The next n elements belonging to the second part and their sum is sumsecond.
The difference in sums of the two parts is denoted as sumfirst - sumsecond.

For example, if sumfirst = 3 and sumsecond = 2, their difference is 1.
Similarly, if sumfirst = 2 and sumsecond = 3, their difference is -1.
Return the minimum difference possible between the sums of the two parts after the removal of n elements.

*/

class Solution {
public:
    long long minimumDifference(vector<int>& nums) {
        long long n=nums.size(),a,b,res=LLONG_MAX;
        vector<long long> AA(n,0),BB(n,0);
        priority_queue<long long> A,B;
        for(long long i=0,tot=0;i<2*n/3+1;i++){
            tot+=nums[i];
            A.push(nums[i]);
            if(A.size()>n/3){
                tot-=A.top();
                A.pop();
            }
            AA[i]=tot;
        }
        for(long long i=n-1,tot=0;i>=n/3;i--){
            tot+=nums[i];
            B.push(-nums[i]);
            if(B.size()>n/3){
                tot+=B.top();
                B.pop();
            }
            BB[i]=tot;
        }
        for(int i=n/3-1;i<2*n/3;i++){
            res=min(res,AA[i]-BB[i+1]);
        }
        return res;
    }
};

/*

2179. Count Good Triplets in an Array

You are given two 0-indexed arrays nums1 and nums2 of length n, both of which are permutations of [0, 1, ..., n - 1].

A good triplet is a set of 3 distinct values which are present in increasing order by position both in nums1 and nums2. In other words, if we consider pos1v as the index of the value v in nums1 and pos2v as the index of the value v in nums2, then a good triplet will be a set (x, y, z) where 0 <= x, y, z <= n - 1, such that pos1x < pos1y < pos1z and pos2x < pos2y < pos2z.

Return the total number of good triplets.

*/

class BIT{
public:
    int tree[100001],n;
    
    BIT(int n){
        this->n=n;
    }
    
    int get(int i,int res=0){
        for(i=i+1;i>0;i-=i&(-i)){
            res+=tree[i];
        }
        return res;
    }
    
    void add(int val,int x){
        for(val=val+1;val<=n;val+=val&(-val)){
            tree[val]+=x;
        }
    } 
};

class Solution {
public:
    long long goodTriplets(vector<int>& nums1, vector<int>& nums2) {
        long long n=nums2.size(),res=0;
        BIT left(n),right(n);
        vector<int> idx_map(n,0);
        for(int i=0;i<n;i++){
            idx_map[nums2[i]]=i;
        }
        
        for(int i:nums2){
            right.add(i,1);
        }
        
        for(int i:nums1){
            int idx=idx_map[i];
            right.add(idx,-1);
            int x=left.get(idx-1),y=right.get(n-1)-right.get(idx);
            res+=x*y;
            left.add(idx,1);
        }
        return res;
    }
};

/*

2246. Longest Path With Different Adjacent Characters

You are given a tree (i.e. a connected, undirected graph that has no cycles) rooted at node 0 consisting of n nodes numbered from 0 to n - 1. The tree is represented by a 0-indexed array parent of size n, where parent[i] is the parent of node i. Since node 0 is the root, parent[0] == -1.

You are also given a string s of length n, where s[i] is the character assigned to node i.

Return the length of the longest path in the tree such that no pair of adjacent nodes on the path have the same character assigned to them.

*/

class Solution {
public:
    int longestPath(vector<int>& parent, string s) {
        vector<vector<int>> tree(s.length(),vector<int>());
        for(int i=0;i<parent.size();i++){
            if(parent[i]!=-1) tree[parent[i]].push_back(i);
        }
        int res=0;
        f(0,tree,s,res);
        return res;
        
    }
    int f(int node,auto& tree,string& s,int& res){
        int a=0,b=0;
        for(int child:tree[node]){
            int x=f(child,tree,s,res);
            if(s[node]!=s[child] && x>a){
                swap(a,b);
                a=x;
            }
            else if(s[node]!=s[child]&& x>b){
                b=x;  
            }
        }
        res=max(res,a+b+1);
        return a+1;
    }
};

/*

2272. Substring With Largest Variance

The variance of a string is defined as the largest difference between the number of occurrences of any 2 characters present in the string. Note the two characters may or may not be the same.

Given a string s consisting of lowercase English letters only, return the largest variance possible among all substrings of s.

A substring is a contiguous sequence of characters within a string.

*/

class Solution {
public:
    int largestVariance(string s) {
        int res=0;
        unordered_set<char> ss(s.begin(),s.end());
        for(char a:ss){
            for(char b:ss){
                if(a!=b) res=max(res,f(a,b,s));
            }
        }
        return res;
    }
    
    int f(char& a,char&b,string& s){
        int leftMin=0,left=0,leftCur=0,cur=0,res=0;
        unordered_map<char,int> cnt;
        for(int i=0;i<s.length();i++){
            if(s[i]==a || s[i]==b) ++cnt[s[i]];
            cur+=s[i]==a ? 1:s[i]==b ? -1:0;
            while(i>left && (s[left]!=a && s[left]!=b || cnt[s[left]]>1)){
                if(s[left]==a || s[left]==b) --cnt[s[left]];
                leftCur+=s[left]==a ? 1:s[left]==b ? -1:0;
                leftMin=min(leftMin,leftCur);
                ++left;
            }
            if(cnt.size()==2){
                res=max(res,cur-leftMin);
            };
        }
        return res;
    }
    
};

/*

2503. Maximum Number of Points From Grid Queries

You are given an m x n integer matrix grid and an array queries of size k.

Find an array answer of size k such that for each integer queries[i] you start in the top left cell of the matrix and repeat the following process:

If queries[i] is strictly greater than the value of the current cell that you are in, then you get one point if it is your first time visiting this cell, and you can move to any adjacent cell in all 4 directions: up, down, left, and right.
Otherwise, you do not get any points, and you end this process.
After the process, answer[i] is the maximum number of points you can get. Note that for each query you are allowed to visit the same cell multiple times.

Return the resulting array answer.

*/

class Solution {
public:
    vector<int> maxPoints(vector<vector<int>>& grid, vector<int>& queries) {
        int m=grid.size(),n=grid[0].size(),rank[100000],par[1000000];
        memset(rank,0,sizeof(rank));
        iota(begin(par),end(par),0);
        
        function<int(int)> find=[&](int x){
            return x==par[x] ? x:par[x]=find(par[x]);
        };
        
        function<void(int,int)> uni=[&](int x,int y){
            int px=find(x),py=find(y);
            if(px==py) return;
            if(py>px) swap(px,py);
            par[py]=px;
            rank[px]+=rank[py];
        };
        
        vector<int> A(m*n),B(queries.size());
        iota(A.begin(),A.end(),0);
        iota(B.begin(),B.end(),0);
        sort(A.begin(),A.end(),[&](int a,int b){
            int ax=a/n,ay=a%n,bx=b/n,by=b%n;
            return grid[ax][ay]<grid[bx][by];
        });
        sort(B.begin(),B.end(),[&](int x,int y){
            return queries[x]<queries[y];
        });
        
        vector<int> res(queries.size(),0);
        int seen[1000][1000],p=0;
        memset(seen,0,sizeof(seen));
        for(int i:B){
            while(p<A.size() && grid[A[p]/n][A[p]%n]<queries[i]){
                int x=A[p]/n,y=A[p]%n;
                ++rank[A[p++]];
                ++seen[x][y];
                for(auto& [xx,yy]:vector<pair<int,int>>{{x+1,y},{x,y+1},{x-1,y},{x,y-1}}){
                    if(0<=xx && xx<m && 0<=yy && yy<n && seen[xx][yy]>0){
                        uni(x*n+y,xx*n+yy);
                    }
                }
            }
            res[i]=rank[find(0)];
        }
        return res;
    }
};

/*

2547. Minimum Cost to Split an Array

You are given an integer array nums and an integer k.

Split the array into some number of non-empty subarrays. The cost of a split is the sum of the importance value of each subarray in the split.

Let trimmed(subarray) be the version of the subarray where all numbers which appear only once are removed.

For example, trimmed([3,1,2,4,3,4]) = [3,4,3,4].
The importance value of a subarray is k + trimmed(subarray).length.

For example, if a subarray is [1,2,3,3,3,4,4], then trimmed([1,2,3,3,3,4,4]) = [3,3,3,4,4].The importance value of this subarray will be k + 5.
Return the minimum possible cost of a split of nums.

A subarray is a contiguous non-empty sequence of elements within an array

*/

class Solution {
public:
    int minCost(vector<int>& nums, int k) {
        int memo[1000];
        memset(memo,-1,sizeof(memo));
        
        function<int(int)> f=[&](int idx){
            if(idx==nums.size()) return 0;
            if(memo[idx]==-1){
                int res=INT_MAX,tot=0;
                unordered_set<int> A,B;
                for(int j=idx;j<nums.size();j++){
                    int x=nums[j];
                    bool y=A.find(x)!=A.end(),z=B.find(x)!=B.end();
                    if(!y && !z){
                        A.insert(x);
                    }
                    else if(y){
                        tot+=2;
                        A.erase(A.find(x));
                        B.insert(x);
                    }
                    else{
                        tot+=1;
                    }
                    res=min(res,tot+k+f(j+1));
                }
                memo[idx]=res;
            }
            return memo[idx];
        };
        
        return f(0);
    }
};

/*

2709. Greatest Common Divisor Traversal

You are given a 0-indexed integer array nums, and you are allowed to traverse between its indices. You can traverse between index i and index j, i != j, if and only if gcd(nums[i], nums[j]) > 1, where gcd is the greatest common divisor.

Your task is to determine if for every pair of indices i and j in nums, where i < j, there exists a sequence of traversals that can take us from i to j.

Return true if it is possible to traverse between all such pairs of indices, or false otherwise.

*/

class Solution {
public:
    int par[100001],rank[100001],primes[100001],n=100000;
    bool canTraverseAllPairs(vector<int>& nums) {
        if(std::find(nums.begin(),nums.end(),1)!=nums.end()){
            return nums.size()==1 && nums[0]==1 ? true:false;
        }
        for(int i=0;i<=n;i++){
            primes[i]=i;
            rank[i]=1;
            par[i]=i;
        }
        for(int i=2;i<=n;i++){
            for(int j=i+i;j<=n;j+=i){
                if(primes[j]==j) primes[j]=i;
            }
        }
        for(int num:nums){
            int prev=num;
            while(num>1){
                int prime=primes[num];
                uni(prev,prime);
                prev=prime;
                while((num%prime)==0) num/=prime;
            }
        }
        unordered_set<int> A;
        for(int i:nums) A.insert(find(i));
        return A.size()==1;
    }
    int find(int x){
        return x==par[x] ? par[x]:par[x]=find(par[x]);
    }
    void uni(int x,int y){
        int px=find(x),py=find(y);
        if(rank[px]>=rank[py]) swap(px,py);
        if(px!=py){
            rank[px]+=rank[py];
            par[py]=px;
        }
    }
    
};

/*

2736. Maximum Sum Queries

You are given two 0-indexed integer arrays nums1 and nums2, each of length n, and a 1-indexed 2D array queries where queries[i] = [xi, yi].

For the ith query, find the maximum value of nums1[j] + nums2[j] among all indices j (0 <= j < n), where nums1[j] >= xi and nums2[j] >= yi, or -1 if there is no j satisfying the constraints.

Return an array answer where answer[i] is the answer to the ith query.

*/

class Solution {
public:
    vector<int> maximumSumQueries(vector<int>& nums1, vector<int>& nums2, vector<vector<int>>& queries) {
        vector<int> A(nums2.size()),B(nums2.begin(),nums2.end()),C(queries.size()),res(queries.size(),-1);
        int tree[400000],p=nums2.size()-1;
        memset(tree,-1,sizeof(tree));
        iota(A.begin(),A.end(),0);
        iota(C.begin(),C.end(),0);
        sort(A.begin(),A.end(),[&](int x,int y){return nums1[x]<nums1[y];});
        sort(B.begin(),B.end());
        sort(C.begin(),C.end(),[&](int x,int y){return queries[x][0]>queries[y][0];});
        
        function<void(int,int,int,int,int)> add=[&](int left,int right,int idx,int pos,int val){
            if(left==right){
                tree[idx]=val;
                return;
            }
            int mid=(left+right)/2;
            if(pos<=mid) add(left,mid,idx*2+1,pos,val);
            else add(mid+1,right,idx*2+2,pos,val);
            tree[idx]=max(tree[idx*2+1],tree[idx*2+2]);
        };
        function<int(int,int,int,int,int)> query=[&](int left,int right,int qleft,int qright,int idx){
            if(left>qright || right<qleft) return -1;
            if(qleft<=left && qright>=right) return tree[idx];
            int mid=(left+right)/2;
            return max(query(left,mid,qleft,qright,idx*2+1),query(mid+1,right,qleft,qright,idx*2+2));
        };
        unordered_map<int,vector<int>> d;
        for(int i=0;i<nums2.size();i++){
            d[B[i]].push_back(i);
        }
        
        for(int i:C){
            int x=queries[i][0],y=queries[i][1];
            while(p>=0 && nums1[A[p]]>=x){
                int ind=A[p--];
                add(0,nums2.size(),0,d[nums2[ind]].back(),nums1[ind]+nums2[ind]);
                d[nums2[ind]].pop_back();
            }
            int idx=lower_bound(B.begin(),B.end(),y)-B.begin();
            res[i]=query(0,nums2.size(),idx,nums2.size(),0);
        }
        return res;
    }
};

/*
2781. Length of the Longest Valid Substring

You are given a string word and an array of strings forbidden.

A string is called valid if none of its substrings are present in forbidden.

Return the length of the longest valid substring of the string word.

A substring is a contiguous sequence of characters in a string, possibly empty.

*/

class Solution {
public:
    int longestValidSubstring(string word, vector<string>& forbidden) {
        const int mod = 1000000007;
        vector<int> A(word.size(), -1);

        auto f = [&](const string& s) {
            long long tar = 0;
            for (char c : s) {
                tar = (tar * 26 + c - 'a') % mod;
            }
            long long cur = 0;
            for (int idx = 0; idx < word.size(); ++idx) {
                cur = (cur * 26 + word[idx] - 'a') % mod;
                if (idx >= s.size() - 1) {
                    if (cur == tar)
                        A[idx] = max(A[idx], idx - (int)s.size() + 2);
                    cur = (cur - powmod(26, s.size() - 1, mod) * (long long)(word[idx - (int)s.size() + 1] - 'a')) % mod;
                    cur = (cur + mod) % mod;
                }
            }
        };

        for (const auto& forb : forbidden) {
            f(forb);
        }

        int res = 0, left = 0;
        for (int i = 0; i < A.size(); ++i) {
            left = max(left, A[i]);
            res = max(res, i - left + 1);
        }

        return res;
    }

private:

    int powmod(long long base, long long exp, int mod) {
        long long result = 1;
        while (exp > 0) {
            if (exp % 2 == 1) {
                result = (result * base) % mod;
            }
            base = (base * base) % mod;
            exp /= 2;
        }
        return result;
    }
};

/*

2953. Count Complete Substrings

You are given a string word and an integer k.

A substring s of word is complete if:

Each character in s occurs exactly k times.
The difference between two adjacent characters is at most 2. That is, for any two adjacent characters c1 and c2 in s, the absolute difference in their positions in the alphabet is at most 2.
Return the number of complete substrings of word.

A substring is a non-empty contiguous sequence of characters in a string.

*/

class Solution {
public:
    int countCompleteSubstrings(string word, int k) {
        
        auto f = [&](int x) {
            int cnt[26];
            memset(cnt,0,sizeof(cnt));
            int found = 0, left = 0, chars = 0,res=0;
            
            for (int idx = 0; idx < word.size(); ++idx) {
                if (idx > 0 && abs(word[idx] - word[idx - 1]) > 2) {
                    memset(cnt,0,sizeof(cnt));
                    found = chars = 0;
                    left = idx;
                }
                
                cnt[word[idx]-'a']++;
                if (cnt[word[idx]-'a'] == k) {
                    found++;
                }
                chars++;
                
                if (found == x) {
                    res++;
                }
                
                if (chars >= k * x) {
                    cnt[word[left]-'a']--;
                    if (cnt[word[left]-'a'] == k - 1) {
                        found--;
                    }
                    left++;
                    chars--;
                }
            }
            
            return res;
        };
        
        int tot=0;
        for (int i = 1; i <= 26; ++i) {
            tot += f(i);
        }
        
        return tot;
    }
};

/*

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

*/

class Solution {
public:
vector<int> beautifulIndices(const string &s, const string &a, const string &b, int k) {
    vector<int> ia = rabin_karp(s, a), ib = rabin_karp(s, b), res;
    for (int i = 0, j = 0; i < ia.size(); ++i) {
        while (j < ib.size() && ib[j] + k < ia[i])
            ++j;
        if (j < ib.size() && abs(ia[i] - ib[j]) <= k)
            res.push_back(ia[i]);
    }
    return res;
}    
vector<int> rabin_karp(string const& s, string const& t) {
    const int p = 31, m = 1e9 + 9, sz = t.size();
    long long p_pow = 1, h_t = 0, h_s = 0;
    for (int i = 0; i < sz; ++i) {
        h_t = (h_t * p + (t[i] - 'a' + 1)) % m;
        p_pow = (p_pow * p) % m;
    }
    vector<int> occurrences;
    for (int i = 0; i < s.size(); ++i) {
        h_s = (h_s * p + (s[i] - 'a' + 1)) % m;
        if (i >= sz)
            h_s = (m + h_s - p_pow * (s[i - sz] - 'a' + 1) % m) % m;
        if (i + 1 >= sz && h_t == h_s)
            occurrences.push_back(i + 1 - sz);
    }
    return occurrences;
  }
};

/*

3041. Maximize Consecutive Elements in an Array After Modification

You are given a 0-indexed array nums consisting of positive integers.

Initially, you can increase the value of any element in the array by at most 1.

After that, you need to select one or more elements from the final array such that those elements are consecutive when sorted in increasing order. For example, the elements [3, 4, 5] are consecutive while [3, 4, 6] and [1, 1, 2, 3] are not.
Return the maximum number of elements that you can select.

*/

class Solution {
public:
    int maxSelectedElements(vector<int>& nums) {
        unordered_map<int,int> dp;
        sort(nums.begin(),nums.end());
        int res=0;
        for(int i:nums){
            res=max(res,dp[i+1]=dp[i]+1);
            res=max(res,dp[i]=dp[i-1]+1);
        }
        return max_element(dp.begin(),dp.end(),[&](auto& a,auto& b){return a.second<b.second;})->second;
    }
};

/*

3045. Count Prefix and Suffix Pairs II

You are given a 0-indexed string array words.

Let's define a boolean function isPrefixAndSuffix that takes two strings, str1 and str2:

isPrefixAndSuffix(str1, str2) returns true if str1 is both a prefix and a suffix of str2, and false otherwise.
For example, isPrefixAndSuffix("aba", "ababa") is true because "aba" is a prefix of "ababa" and also a suffix, but isPrefixAndSuffix("abc", "abcd") is false.

Return an integer denoting the number of index pairs (i, j) such that i < j, and isPrefixAndSuffix(words[i], words[j]) is true.

*/

struct TrieNode{
    unordered_map<int,TrieNode*> children;
    int freq=0,idx=-1;
};

struct Trie{
    TrieNode* root=new TrieNode();
    
    void add(string& word,int idx){
        TrieNode* node=root;
        for(char& c:word){
            if(node->children.count(c)==0){
                node->children.insert({c,new TrieNode()});
            }
            node=node->children[c];
        }
        ++(node->freq);
        node->idx=idx;
    }
    int get(string& word,unordered_set<int>& seen){
        TrieNode* node=root;
        int res=0;
        for(char& c:word){
            if(node->children.count(c)!=0){
                node=node->children[c];
                res+=(node->idx==-1 ? 0:1)*(node->freq)*(seen.count(node->idx));
                seen.insert(node->idx);
            }
            else break;
        }
        return res;
    } 
};

class Solution {
public:
    long long countPrefixSuffixPairs(vector<string>& words) {
        long long res=0;
        Trie pref,suf;
        int idx=0;
        for(string& word:words){
            unordered_set<int> seen;
            string rev=word;
            reverse(rev.begin(),rev.end());
            res+=pref.get(word,seen)*0+suf.get(rev,seen);
            pref.add(word,idx);
            suf.add(rev,idx);
            ++idx;
        }
        return res;
    }
};

/*

3113. Find the Number of Subarrays Where Boundary Elements Are Maximum

You are given an array of positive integers nums.

Return the number of subarrays of nums, where the first and the last elements of the subarray are equal to the largest element in the subarray.

*/

class Solution {
public:
    long long numberOfSubarrays(vector<int>& nums) {
        deque<int> A;
        long long res=0;
        for(int num:nums){
            while(!A.empty() && A[0]<num) A.pop_front();
            A.push_front(num);
            int left=lower_bound(A.begin(),A.end(),num)-A.begin();
            int right=upper_bound(A.begin(),A.end(),num)-A.begin();
            res+=right-left;
        }
        return res;
    }
};

/*

3117. Minimum Sum of Values by Dividing Array

You are given two arrays nums and andValues of length n and m respectively.

The value of an array is equal to the last element of that array.

You have to divide nums into m disjoint contiguous subarrays such that for the ith subarray [li, ri], the bitwise AND of the subarray elements is equal to andValues[i], in other words, nums[li] & nums[li + 1] & ... & nums[ri] == andValues[i] for all 1 <= i <= m, where & represents the bitwise AND operator.

Return the minimum possible sum of the values of the m subarrays nums is divided into. If it is not possible to divide nums into m subarrays satisfying these conditions, return -1.

*/

class Solution {
public:
    int minimumValueSum(vector<int>& nums, vector<int>& andValues) {
        int n=nums.size(),m=andValues.size();
        vector<vector<int>> A(nums.size(),vector<int>(18,n));
        vector<int> closest(18,n);
        
        for(int i=n-1;i>=0;i--){
            for(int j=0;j<18;j++){
                int bit=(nums[i]>>j)&1;
                if(bit==0) closest[j]=i;
                A[i][j]=closest[j];
            }
        }
        
        int memo[10000][10][2];
        memset(memo,-1,sizeof(memo));
        
        function<int(int,int,int)> f=[&](int i,int j,int start){
            if(i==n || j==m){
                return i==n && j==m && start==1 ? 0:(int)1e6;
            }
            if(start && memo[i][j][start]==-1){
                int mx=n,mn=i;
                for(int k=0;k<18;k++){
                    int bit=(andValues[j]>>k)&1;
                    if(bit) mx=min(mx,A[i][k]);
                    else mn=max(mn,A[i][k]);
                }
                memo[i][j][start]=mn<=mx ? f(mn,j,0):(int)1e6;
            }
            else if(start==0 && memo[i][j][start]==-1){
                bool check=false;
                for(int k=0;k<18;k++){
                    if((andValues[j]>>k)&1 && ((nums[i]>>k)&1)==0) check=true;
                }
                memo[i][j][start]=check==true ? (int)1e6:min(nums[i]+f(i+1,j+1,1),f(i+1,j,0));
            }
            return memo[i][j][start];
        };
        
        int res=f(0,0,1);
        return res>=1e6 ? -1:res;
    }
};

/*
862. Shortest Subarray with Sum at Least K

Given an integer array nums and an integer k, return the length of the shortest non-empty subarray of nums with a sum of at least k. If there is no such subarray, return -1.

A subarray is a contiguous part of an array.
*/

class Solution {
public:
    int shortestSubarray(vector<int>& nums, int k) {
        vector<long long> A(nums.size()+1,0),B(nums.size()+1,0);        
        for(int i=0;i<nums.size();i++){
            A[i+1]=A[i]+nums[i];
        }
        iota(B.begin(),B.end(),0);              
        sort(B.begin(),B.end(),[&](auto x,auto y){return A[x]<A[y];});

        multiset<int> C;
        long long res=-1,p=0;
        for(int idx:B){
            long long i=A[idx];
            while(A[B[p]]<=i-k){
                C.insert(B[p++]);
            }
            auto j=C.lower_bound(idx);
            if(j!=C.begin()){
                long long cur=abs(idx-*prev(j));
                if(res==-1 || res>-1 && cur<res) res=cur;
            } 
        }
        return res;
    }
};

/*
2552. Count Increasing Quadruplets

Given a 0-indexed integer array nums of size n containing all numbers from 1 to n, return the number of increasing quadruplets.

A quadruplet (i, j, k, l) is increasing if:

0 <= i < j < k < l < n, and
nums[i] < nums[k] < nums[j] < nums[l].

*/

class Solution {
public:
    long long countQuadruplets(vector<int>& nums) {
        int n = nums.size();
        vector<int> small(4 * n, 0), big(4 * n, 0);
        unordered_map<int, int> idx;
        
        for (int i = 0; i < n; ++i) {
            idx[nums[i]] = i;
        }
        
        auto addVal = [](vector<int>& tree, int idx, int val) {
            ++idx;
            while (idx < tree.size()) {
                tree[idx] += val;
                idx += idx & (-idx);
            }
        };
        
        auto getVal = [](vector<int>& tree, int idx) {
            ++idx;
            int val = 0;
            while (idx > 0) {
                val += tree[idx];
                idx -= idx & (-idx);
            }
            return val;
        };
        
        long long res = 0;
        for (int k = 1; k <= n; ++k) {
            fill(big.begin(), big.end(), 0);
            for (int j = n; j > k; --j) {
                int ki = idx[k], ji = idx[j];
                if (ji < ki) {
                    long long left = getVal(small, ji - 1);
                    long long right = getVal(big, n - 1) - getVal(big, ki);
                    res += left * right;
                }
                addVal(big, idx[j], 1);
            }
            addVal(small, idx[k], 1);
        }
        return res;
    }
};

/*

1862. Sum of Floored Pairs

Given an integer array nums, return the sum of floor(nums[i] / nums[j]) for all pairs of indices 0 <= i, j < nums.length in the array. Since the answer may be too large, return it modulo 109 + 7.

The floor() function returns the integer part of the division.

*/

class Solution {
public:
    static constexpr int mod = 1'000'000'007;
    
    int sumOfFlooredPairs(vector<int>& nums) {
        int mx = *max_element(nums.begin(), nums.end());
        long long res = 0;
        vector<int> tree(4 * mx, 0);
        unordered_map<int, int> cnt;
        
        for (int num : nums) {
            cnt[num]++;
        }
        
        auto addVal = [&](int idx, int val) {
            idx++;
            while (idx < tree.size()) {
                tree[idx] += val;
                idx += idx & (-idx);
            }
        };
        
        auto getVal = [&](int idx) {
            long long sum = 0;
            idx++;
            while (idx > 0) {
                sum += tree[idx];
                idx -= idx & (-idx);
            }
            return sum;
        };
        
        for (int num : nums) {
            addVal(num, 1);
        }
        
        for (int i = 1; i <= mx; i++) {
            int freq = cnt[i];
            if (freq == 0) continue;
            
            for (int j = i; j <= mx; j += i) {
                int d = j / i;
                int left = max(0, j);
                int right = min(mx, j + i - 1);
                long long tot = getVal(right) - getVal(left - 1);
                res = (res + (long long)freq * tot * d) % mod;
            }
        }
        
        return res;
    }
};

