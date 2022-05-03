# iterates through array swapping elements to find the smallest.
def bubbleSort(arr): 
  n = len(arr) 
  for i in range(n): 
    for j in range(0, n-i-1): 
      if arr[j] > arr[j+1] : 
        arr[j], arr[j+1] = arr[j+1], arr[j] 
 
# inserts every array element into its proper position by shifting numbers.
def insertionSort(arr): 
  for i in range(1, len(arr)): 
    key = arr[i] 
    j = i-1
    while j >= 0 and key < arr[j]: 
      arr[j + 1] = arr[j] 
      j -= 1
    arr[j + 1] = key 

# iterates through array finding smallest element to insert.
def selectionSort(arr): 
  for i in range(len(arr)): 
    min_idx = i 
    for j in range(i+1, len(arr)): 
      if arr[min_idx] > arr[j]: 
        min_idx = j 
    arr[i], arr[min_idx] = arr[min_idx], A[i] 

# QuickSort
def quickSort(arr,low,high): 
  if low < high: 
    pi = partition(arr,low,high) 
    quickSort(arr, low, pi-1) 
    quickSort(arr, pi+1, high) 

def partition(arr,low,high): 
  i = low - 1
  pivot = arr[high]
  for j in range(low , high): 
    if arr[j] <= pivot: 
      # increment index of smaller element 
      i = i+1
      # swap
      arr[i], arr[j] = arr[j], arr[i] 
  arr[i+1], arr[high] = arr[high], arr[i+1] 
  return i + 1

a = [1,3,5,2,4]
quickSort(a, 0, 4)
print(a)
