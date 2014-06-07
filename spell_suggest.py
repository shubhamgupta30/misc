# From http://norvig.com/spell-correct.html
#

import re
import collections

def words(text): return re.findall('[a-z]+', text.lower())

def train (features):
  # Default value is set to 1 to take care of novel words - words which we have
  # not seen in the train data. 
  model = collections.defaultdict(lambda: 1)
  for f in features:
    model[f] += 1
  return model

NWORDS = train(words(file('big.txt').read()))

alphabet = "abcdefghijklmnopqrstuvwxyz"

# Words which are edit distance 1 from the given word
def edits1(word):
  splits = [(word[:i], word[i:]) for i in xrange(len(word)+1)]
  inserts = [a+c+b for a,b in splits for c in alphabet]
  deletes = [a + b[1:] for a,b in splits if b]
  alteration = [a + c + b[1:] for a,b in splits for c in alphabet if b]
  transposes = [a[:-1] + b[0] + a[-1] + b[1:] for a,b in splits if a and b]
  return set(inserts + deletes + alteration + transposes)
