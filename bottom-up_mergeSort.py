#bottom up implementation of merge sort algorithm

import numpy

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

print(mergeSort(A)) 
