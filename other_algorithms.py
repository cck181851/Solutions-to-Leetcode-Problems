import numpy,math,itertools,time

#bottom up implementation of merge sort algorithm 

A=[numpy.random.randint(1,100) for _ in range(30)]

def mergeSort(A):
    width=1 
    while width<len(A):
        for i in range(0,len(A),width*2):
            mid=min(i+width-1,len(A)-1) 
            high=min(mid+width,len(A)-1) 
            merge(A,i,mid,high)
        width*=2 
    return A 

def merge(A,low,mid,high):
    cnt=[0]*(high-low+1)
    i,j,k=low,mid+1,0 
    while i<=mid and j<=high:
        cnt[k]=min(A[i],A[j])
        k+=1 
        if A[i]<=A[j]:i+=1 
        else:j+=1 
    while i<=mid:
        cnt[k]=A[i]
        i,k=i+1,k+1 
    while j<=high:
        cnt[k]=A[j]
        j,k=j+1,k+1 
    for i in range(low,high+1):
        A[i]=cnt[i-low]

#print(mergeSort(A)) 

#--------------------------------------------------------

#solution to unresolved recursive calls problem of quick sort algorithm

def quickSort(A,low,high):
    while low<high:
        idx=partition(A,low,high)
        if (high-idx)>(idx-low):
            quickSort(A,low,idx-1)
            low=idx+1
        else:    
            quickSort(A,idx+1,high)
            high=idx-1

def partition(A,low,high):
    pivot=A[low]
    i=low 
    for j in range(low+1,high+1):
        if A[j]<pivot:
            A[i],A[j]=A[j],A[i]
            i+=1      
    A[i]=pivot 
    return i 

#quickSort(A,0,len(A)-1)
#print(A)  

#------------------------------------------------------------

#quickSort algorithm generalized for any pivot

def quickSort(A,low,high):
    if low<high: 
        pivot=select(A,low,high)
        quickSort(A,low,pivot-1)
        quickSort(A,pivot+1,high)
    
def select(A,low,high):
    left=low-1 
    pivot_index=(low+high)//2
    pivot=A[pivot_index]
    for i in range(low,high+1):
        if A[i]<=pivot:
            if A[i]==pivot:
                pivot_index=left+1
            A[left+1],A[i]=A[i],A[left+1]
            left+=1 
    A[pivot_index],A[left]=A[left],A[pivot_index]    
    return left
    
quickSort(A,0,len(A)-1)
#print(A)

#--------------------------------------------------------
#bingo sort implementation

def bingoSort(A):
    minValue=min(A)
    maxValue=max(A)
    bingo=minValue 
    nextBingo=maxValue 
    nextAvail=0
    while bingo<maxValue:
        for i in range(nextAvail,len(A)):
            if A[i]==bingo:
                A[nextAvail],A[i]=A[i],A[nextAvail]
                nextAvail+=1
            elif A[i]<nextBingo:
                nextBingo=A[i]
        bingo=nextBingo 
        nextBingo=maxValue 

#bingoSort(A)
#print(A) 

#-------------------------------------------------------
#shell sort implementation

def insertionSubSort(A,k):
    for i in range(k,len(A)):
        cur=A[i]
        j=i-k 
        while j>=0 and A[j]>cur:
            A[j+k]=A[j]
            j=j-k 
        A[j+k]=cur 

def shellSort(A,L):
    for i in L:
        insertionSubSort(A,i)

#shellSort(A,[16,8,4,2,1])
#print(A)  

#--------------------------------------------------------
#efficient radix sort implementation using linked lists

import math,numpy

class listNode:
    def __init__(self,val=None,next=None):
        self.val=val 
        self.next=next 

#get the digit at the index i,pad the left part with 0's if needed 
def getDigit(s,i):    
    s="0"*(10-len(s)+1)+s 
    try:
        return int(s[i])
    except:
        return 0


def radixSort(A):    
    for idx in range(10,-1,-1):
        front=[None for _ in range(10)]
        back=[None for _ in range(10)]        
        while A:
            num=A.val
            val=getDigit(str(num),idx)
            cur=listNode(num)
            if front[val] is None:
                front[val]=back[val]=cur
            else:
                back[val].next=cur 
                back[val]=cur 
            A=A.next
        p=0 
        while front[p]==None:
            p=p+1
        start=front[p]
        pre=p
        while p<len(front):
            p=p+1
            while p<len(front) and front[p]==None:
                p+=1 
            if p<len(front):
                back[pre].next=front[p]
                pre=p
        A=start       
    return A    
       
#create the list
A=listNode(-1)
start=A
for _ in range(1000):
    node=listNode(numpy.random.randint(1,1000))
    A.next=node 
    A=node

#sort the list 
node=radixSort(start.next)

#check whether it works correctly
B=[]
while node:
    B+=[node.val]
    node=node.next
print(B==sorted(B))

#-------------------------------------------------------

#iterative implementation of DFS

graph=[[],[2,3,8,9],[1,3,4,7],[1,2,4],[2,3,5,6,7],[4,6],[5,9],[2,4,8],[1,7],[1,6]]
visited={7}

def next(node):
    for i in graph[node]:
        if i not in visited:
            return i 
    return None 
    
node=7    
stack=[]   
nxt=next(node)

while nxt or stack:
    if nxt:
        stack+=[node]
        visited.add(nxt)        
        node=nxt
        #print(node)
    else:
        node=stack.pop()
    nxt=next(node)

#recursive version

visited=set()
def dfs(node):
    if node in visited:
        return 
    #print(node)
    visited.add(node)
    for nxt in A[node]:
        dfs(nxt)
    
dfs(7)   

#-------------------------------------------------

#bfs implementation

A=[[],[2,3,8,9],[1,3,4,7],[1,2,4],[2,3,5,6,7],[4,6],[5,9],[2,4,8],[1,7],[1,6]]
queue=collections.deque([7])
visited=set() 

while queue:
    node=queue.popleft()
    if node in visited:
        continue 
    visited.add(node)
    #print(node)
    for nxt in A[node]:
        if nxt not in visited:
            queue.append(nxt)
    








