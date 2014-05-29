import array
import heapq
import random
import time
import tempfile

def generate_random_numbers(filename, size):
  start = time.clock()
  with open(filename, 'w') as f:
    for i in  xrange(size):
      f.write(str(random.randint(0, 2**31)))
      f.write('\n')
  end = time.clock()
  print "Generated and wrote %d integers in %f seconds"%(size, end-start)


def process_string(s, leftover):
  a = s.split('\n')
  a[0] = leftover + a[0]
  leftover = a[-1]
  a = [int(x) for x in a[:-1]]
  return a, leftover

def intsfromfile(f, chunk):
  leftover = ''
  while True:
     a, leftover = process_string(f.read(chunk), leftover)
     if not a and leftover == '':
         break
     for x in a:
         yield x

def create_and_sort_chunks(f, max_size_per_file, read_buffer_size):
  iters = []
  leftover = ''
  while True:
     a, leftover = process_string(f.read(max_size_per_file), leftover)
     if not a and leftover == '':
         break
     temp_f = tempfile.TemporaryFile()
     f_string = '\n'.join(str(x) for x in sorted(a))
     f_string += "\n"
     temp_f.write(f_string)
     temp_f.seek(0)
     iters.append(intsfromfile(temp_f, read_buffer_size))
     print len(iters)
  print "Created %d temporary files" % len(iters)
  return iters

if __name__ == "__main__":
  with open('sorted_random_integers', 'w') as f_out:
    with open('random_integers', 'r') as f_in:
      iters = create_and_sort_chunks(f_in, 400000, 4000)
      sorted_ints = []
      count = 0
      for x in heapq.merge(*iters):
        sorted_ints.append(x)
        if len(sorted_ints) >= 1000:
          f_out.write('\n'.join(str(x) for x in sorted_ints))
          f_out.write("\n")
          count += len(sorted_ints)
          print count
          sorted_ints = []
      if sorted_ints:
        f_out.write('\n'.join(str(x) for x in sorted_ints))
        f_out.write("\n")
      print "All sorted numbers written"
