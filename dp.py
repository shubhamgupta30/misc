# Contiguous subarray with some condition on sum
#
def conditional_sum(A, condition):
  conditional_sum_so_far = A[0]
  start = 0
  end = 0
  running_sum = A[0]
  running_start = 0
  for i in xrange(1,len(A)):
    if condition(A[i],running_sum + A[i]):
      running_sum = A[i]
      running_start = i
    else :
      running_sum += A[i]
    if condition(running_sum, conditional_sum_so_far):
      conditional_sum_so_far = running_sum
      start = running_start
      end = i
  return conditional_sum_so_far, start, end

# Largest sum
#
def largest_sum(A):
  def condition(sum1, sum2):
    return sum1 > sum2
  return conditional_sum(A, condition)

# Sum closest to k
#
def closest_to_k(A, k):
  def condition(sum1, sum2):
    return abs(sum1 - k) < abs(sum2 - k)
  return conditional_sum(A, condition)

# Sum closest to 0
#
def closest_to_0(A):
  return closest_to_k(A, 0)

# 
