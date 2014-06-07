""" How many minimum insertions needed to get a pallindrome
Args:
  input_str: Input string to be converted to pallindrome
"""
def convertToPallindrome(input_str):
  if input_str == "":
    return 0
  l = len(input_str)
  DP_table = {}
  for i in xrange(l):
    DP_table[(i,i)] = 0
  for j in xrange(1,l):
    for i in xrange(l-j):
      r = i
      c = i + j
      # Filling DP_table(r,c)
      if input_str[r] == input_str[c]:
        DP_table[(r,c)] = DP_table[(r+1, c-1)]
      else:
        DP_table[(r, c)] = min(DP_table[(r+1, c)], DP_table[(r, c-1)]) + 1
    
  print DP_table[(0,l-1)], reconstruct(DP_table, input_str)
  return

""" Reconstruct the pallindrome
"""
def reconstruct(DP_table, S):
  output = ""
  i = 0
  j = len(S)-1
  while i < j:
    if S[i] == S[j]:
      output += S[j]
      i += 1
      j -= 1
      continue
    if DP_table[(i,j)] == DP_table[(i+1, j)] + 1:
      output += S[i]
      i += 1
      continue
    output += S[j]
    j -= 1
  return output

if __name__ == "__main__":
  convertToPallindrome(raw_input())

