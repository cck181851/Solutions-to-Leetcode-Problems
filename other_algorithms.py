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

#print(mergeSort(A)) 

#--------------------------------------------------------

#solution to unresolved recursive calls problem

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
