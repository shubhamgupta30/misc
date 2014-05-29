## Implementing a good quicksort.
import random
import time
import pylab

def quicksort (A, lo, hi, k):
  # Stop when each element is atmost k hops away from final destination
  if hi - lo > max(k,0):
    # Get a good pivot
    p = pivot(A, lo, hi)
    # Partition intelligently to avoid bad performance when lots of repeating
    # entries.
    left, right = partition(A, lo, hi, p)
    # get the smaller range to recurse on first.
    if left - lo < hi < right:
      small = (lo, left)
      large = (right, hi)
    else:
      large = (lo, left)
      small = (right, hi)
    # Acoid extra recursion if no need
    if small[1] - small[0] > max(k,0):
      quicksort(A, small[0], small[1], k)
    if large[1] - large[0] > max(k,0):
      quicksort(A, large[0], large[1], k)


def pivot(A, lo, hi):
  return A[random.randint(lo, hi)]

def insertionsort(A, lo, hi):
  if hi - lo <= 1:
    return
  wall = lo
  while wall < hi:
    j = wall + 1
    while j > 0 and A[j-1] > A[j]:
        swap(A, j-1, j)
        j -= 1
    wall += 1


def partition(A, lo, hi, p):
  # Three locations:
  # First element from left not < p : ptr1
  # First element from the left of ptr1 not = p: ptr2
  # First element from the right not > p: ptr3
  # Traverse the array from left to right
  ptr1 = lo
  ptr2 = lo
  ptr3 = hi
  while ptr3 >= ptr2:
    if A[ptr2] < p:
      swap(A, ptr1, ptr2)
      ptr1 += 1
      ptr2 += 1
    elif A[ptr2] == p:
      ptr2 += 1
    else:
      swap(A, ptr2, ptr3)
      ptr3 -= 1
  return ptr1-1, ptr3+1

def swap(A, ptr1, ptr2):
  temp = A[ptr1]
  A[ptr1] = A[ptr2]
  A[ptr2] = temp

def find_k(num_tries = 100, size = 10000, k_max = 10):
  qs_times = [0]*k_max
  is_times = [0]*k_max
  inline_is_times = [0]*k_max
  for i in xrange(num_tries):
    B = random.sample(range(size*10), size)
    for k in xrange(0,k_max):
      A = [item for item in B]
      start_time = time.clock()
      quicksort(A, 0, size-1, k)
      qs_time = time.clock()
      insertionsort(A, 0, len(A)-1)
      is_time = time.clock()
      qs_times[k] += qs_time - start_time
      is_times[k] += is_time - qs_time

  qs_times = [float(total)/float(num_tries) for total in qs_times]
  is_times = [float(total)/float(num_tries) for total in is_times]
  total_times = [x+y for x,y in zip(qs_times, is_times)]
  pylab.plot(range(k_max), qs_times)
  pylab.plot(range(k_max), is_times)
  pylab.plot(range(k_max), total_times)
  pylab.show()
  return qs_times, is_times, total_times





