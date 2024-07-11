"""
  1766. Tree of Coprimes
There is a tree (i.e., a connected, undirected graph that has no cycles) consisting of n nodes numbered from 0 to n - 1 and exactly n - 1 edges. Each node has a value associated with it, and the root of the tree is node 0.

To represent this tree, you are given an integer array nums and a 2D array edges. Each nums[i] represents the ith node's value, and each edges[j] = [uj, vj] represents an edge between nodes uj and vj in the tree.

Two values x and y are coprime if gcd(x, y) == 1 where gcd(x, y) is the greatest common divisor of x and y.

An ancestor of a node i is any other node on the shortest path from node i to the root. A node is not considered an ancestor of itself.

Return an array ans of size n, where ans[i] is the closest ancestor to node i such that nums[i] and nums[ans[i]] are coprime, or -1 if there is no such ancestor.
"""

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
