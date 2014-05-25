# Binary search can be used to search over any function that is monotonous
# (not necessarily strictly). It ususally is used when we are given an
# increasing function and we are supposed to invert it.
# e.g.
# * In an array,
#   - find one location where k occurs,
#   - find the first location where k occurs,
#   - find the third location where k occurs, etc.
# * Find floor of square root of a 32 bit integer
#
# A general framework is:
"""
" l : The lower bound 
" u :  upper bound
" Required: l <= u, otherwise it returns "None"
" condition_equal: Specifies the condition to check when we can declare success
" condition_greater: condition where we have overshot the inverse
" condition_lesser: condition where we are below the inverse
" Note that we do not need all these three conditions as they must ideally be
" mutually exclusive and exhaustive. Thus we have ommitted the last one.
" debug: Displays debug information about iterations if set to True
"""
def BinSearch(l, u, condition_equal, condition_greater, debug=False):
  while l <= u:
    m = l + (u-l)/2
    if debug: print "l = %d, m = %d, u = %d" % (l, m, u)
    if condition_equal(m):
      if debug: print "met condition. Answer = %d" %(m)
      return m
    if condition_greater(m):
      u = m-1
    else:
      l = m+1
  if debug: print "Search Failed"
  return None

#############################################
# Some Examples. 
#############################################

# 1. Search a sorted array A for an occurence of element k
def searchSortedArray(A, k):
  def cequal(m):
    return A[m] == k
  def cgreater(m):
    return A[m] > k
  return BinSearch(0, len(A) - 1, cequal, cgreater, True)

# 2. Search a sorted array A for first occurence of element k
def getFirstOccurence(A, k):
  def cequal(m):
    return (m == 0 and A[m] == k) or (A[m-1] != k and A[m] == k)
  def cgreater(m):
    return (m == 0 and A[m] > k) or A[m-1] >= k
  return BinSearch(0, len(A)-1, cequal, cgreater, True)

# 3. Search a sorted array A for last occurence of element k
def getLastOccurence(A,k):
  def cequal(m):
    return (m == len(A)-1 and A[m] == k) or (A[m] == k and A[m+1] != k)
  def cgreater(m):
    return A[m] > k
  return BinSearch(0, len(A)-1, cequal, cgreater, True)

# 4. Integer square root of a 32 bit integer
def SqRoot(n):
  def cequal(m):
    return m*m <= n and (m+1)*(m+1) > n
  def cgreater(m):
    return m*m > n
  return BinSearch(0, 2**16-1, cequal, cgreater, True)
