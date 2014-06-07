"""Naive implementation of multiplication
Args:
  number1: first number as string
  number2: second number as string
"""
def multiplyNaive(number1, number2):
  n1 = [int(i) for i in number1][::-1]
  n2 = [int(i) for i in number2][::-1]
  results = []
  for index, n in enumerate(n2):
    row = [n*i for i in n1]
    carry = 0
    for j in xrange(len(row)-1):
      r = row[j] + carry
      row[j] = r%10
      carry = r/10
    row[-1] += carry
    results.append("".join(map(str, row)[::-1]) + "0"*index)
  return addNaive(results)

"""Adds a list of numbers
Args:
  numbers: list of strings. Each string represents a number.
Returns:
  Sum of these numbers represented as list
"""
def addNaive(numbers):
  if len(numbers) == 1:
    return numbers[0]
  def add_two(number1, number2):
    n1 = [int(i) for i in number1][::-1]
    n2 = [int(i) for i in number2][::-1]
    result = [0]*max(len(n1), len(n2))
    for i in xrange(len(result)):
      if i < len(n1): result[i] += n1[i]
      if i < len(n2): result[i] += n2[i]
    carry = 0
    for j in xrange(len(result)-1):
      temp = carry + result[j]
      result[j] = temp%10
      carry = temp/10
    result[-1] += carry
    return "".join(map(str, result)[::-1])
  final_sum = numbers[0]
  for i in xrange(1,len(numbers)):
    final_sum = add_two(final_sum, numbers[i])
  return final_sum


if __name__ == "__main__":
  print multiplyNaive(raw_input(), raw_input())

  
