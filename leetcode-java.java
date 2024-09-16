/*
Min Cost to Connect All Points
You are given an array points representing integer coordinates of some points on a 2D-plane, where points[i] = [xi, yi].

The cost of connecting two points [xi, yi] and [xj, yj] is the manhattan distance between them: |xi - xj| + |yi - yj|, where |val| denotes the absolute value of val.

Return the minimum cost to make all points connected. All points are connected if there is exactly one simple path between any two points.
*/  

class Solution {
    public int minCostConnectPoints(int[][] points) {
        ArrayList<int[]>[] A=new ArrayList[points.length];
        for(int i=0;i<points.length;i++){
            A[i]=new ArrayList<int[]>();
        }

        for(int i=0;i<points.length;i++){
            for(int j=i+1;j<points.length;j++){
                int d=dist(i,j,points);
                A[i].add(new int[]{d,j});
                A[j].add(new int[]{d,i});
            }
        }
        PriorityQueue<int[]> q=new PriorityQueue<>((a,b)->a[0]-b[0]);
        HashSet<Integer> seen=new HashSet<>();
        int res=0;
        q.offer(new int[]{0,0});
        while(!q.isEmpty() && seen.size()<points.length){
            int t[]=q.poll(),d=t[0],node=t[1];
            if(!seen.add(node)) continue;
            res+=d;
            for(int[] x:A[node]){
                if(!seen.contains(x[1])){
                    q.offer(new int[]{x[0],x[1]});
                }
            }
        }
        return res;
    }
    int dist(int x,int y,int[][] points){
        int x1=points[x][0],y1=points[x][1];
        int x2=points[y][0],y2=points[y][1];
        return Math.abs(x1-x2)+Math.abs(y1-y2);
    }
}

/*
2935. Maximum Strong Pair XOR II

You are given a 0-indexed integer array nums. A pair of integers x and y is called a strong pair if it satisfies the condition:

|x - y| <= min(x, y)
You need to select two integers from nums such that they form a strong pair and their bitwise XOR is the maximum among all strong pairs in the array.

Return the maximum XOR value out of all possible strong pairs in the array nums.

Note that you can pick the same integer twice to form a pair.
*/

class TrieNode {
    TrieNode[] children = new TrieNode[2];
    int min = Integer.MAX_VALUE;
    int max = Integer.MIN_VALUE;
}

class Solution {
    TrieNode root = new TrieNode();    
    public int maximumStrongPairXor(int[] nums) {
        int res = 0;
        for (int num : nums) {
            insert(num);
        }
        for (int num : nums) {
            int res = find(num, num * 2);
            res = Math.max(res, num ^ res);
        }
        return res;
    }
    
    public void insert(int num) {
        TrieNode node = root;
        for (int i = 20; i >= 0; i--) {
            int bit = (num >> i) & 1;
            if (node.children[bit] == null) {
                node.children[bit] = new TrieNode();
            }
            node = node.children[idx];
            node.min = Math.min(node.min, num);
            node.max = Math.max(node.max, num);
        }
    }
    
    public int find(int num, int range) {
        TrieNode node = root;
        int res = 0;
        for (int i = 20; i >= 0; i--) {
            int a = (num >> i) & 1;
            int b = 1 - a;
            if (node.children[b] != null && node.children[b].min <= range && node.children[b].max > num) {
                res = res | b << i;
                node = node.children[b];
            } else {
                res = res | a << i;
                node = node.children[a];
            }
        }
        return res;
    }
}


