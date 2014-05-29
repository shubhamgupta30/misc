import array
import random
import time

def generate_random_numbers(filename, size):
  start = time.clock()
  f = open(filename, 'w')
  for i in  xrange(size):
    f.write(str(random.randint(0, 2**31)))
    f.write('\n')
  f.close()
  end = time.clock()
  print "Generated and wrote %d integers in %f seconds"%(size, end-start)


def process_string(s, leftover):
  a = s.split('\n')
  a[0] = leftover + a[0]
  return a[:-1], a[-1]

def intsfromfile(f, chunk):
  leftover = ''
  while True:
     a, leftover = process_string(f.read(chunk), leftover)
     if not a and leftover == '':
         break
     for x in a:
         yield x

