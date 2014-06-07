import queue

# Graph represented as a dictionary with keys as vertices and the values as list of vertices
# adjacent to it

# Computes reachable nodes and calcualtes their shortest distance from the start node
def BFS(graph, start):
  visited = {}
  q = queue.Queue()
  q.put((start,0))
  while not q.empty():
    node, index = q.get()
    if node not in visited:
      visited[node] = index
      for neighbor in graph[node]:
        q.put((neighbor, index + 1))
  return visited

# Depth First Search
def DFS(graph, start):
  dfs_tree = {start : []}
  stack = queue.LifoQueue()
  stack.put((start, None))
  while not stack.empty():
      node, parent = stack.get()
      if node not in dfs_tree and parent != None:
          dfs_tree[node] = [parent]
          dfs_tree[parent].append(node)
      for child in graph[node]:
          if child not in dfs_tree:
            stack.put((child, node))
  return dfs_tree

# Number of components
def components(graph):
  visited = {}
  count = 0
  for node in graph:
    if node not in visited:
      component = BFS(graph, node)
      for cnode in component: visited[cnode] = True
      print(component)
      count += 1
  return count

# True if there is an Eulerian Tour in the undirected graph
def contains_eulerian_tour_undirected(graph):
  for vertex in graph:
    if len(vertex) % 2 != 0:
      return False
  return True

# True if there is an Eulerian Tour in the directed graph
def contains_eulerian_tour_directed(graph):
  # construct complement
  g_complement = {}
  for (vertex, neighbor) in [(v,n) for n in graph[v] for v in graph]:
    g_complement.setdefault(n,[])
    g_complement[n].append(v)
  for vertex in graph:
    if len(graph[vertex]) != len(g_complement[vertex]):
      return False
  return True


def tree_level_wise_traversal(tree, root):
  q = queue.Queue()
  q.put(root)
  traversal = []
  visited = {}
  while not q.empty():
    node = q.get()
    traversal.append(node)
    visited[node] = True
    for child in [c for c in tree[node] if c not in visited]:
      q.put(child)
  return traversal

def tree_diameter(tree):
  root = list(tree.keys())[0]
  traversal = tree_level_wise_traversal(tree, root)[::-1]
  print(traversal)
  diameter_and_depth = {}
  for node in traversal:
    if len(tree[node]) == 1 and node != root:
      # Leaf
      diameter_and_depth[node] = (0, 0)
      continue
    diam = 0
    depth = 0
    child_diams_and_depths = [diameter_and_depth[c] for c in tree[node] if c in diameter_and_depth]
    def top_two(l):
      x1, x2 = min(l), min(l)
      for n in l:
        if n > x1:
          x1, x2 = n, x1
        elif n > x2:
          x1, x2 = x1, n
      return [x1, x2]
    def composed_diam():
      if len(child_diams_and_depths) == 1:
        return child_diams_and_depths[0][1] + 1
      return sum(top_two([value[1] for value in child_diams_and_depths])) + 2
    diam = max([values[0] for values in child_diams_and_depths] + [composed_diam()])
    depth = max([values[1] for values in child_diams_and_depths]) + 1
    diameter_and_depth[node] = (diam, depth)
  return diameter_and_depth, root


class MyHeap(object):
   def __init__(self, initial=None, key=lambda x:x):
       self.key = key
       if initial:
           self._data = [(key(item), item) for item in initial]
           heapq.heapify(self._data)
       else:
           self._data = []

   def push(self, item):
       heapq.heappush(self._data, (self.key(item), item))

   def pop(self):
       return heapq.heappop(self._data)[1]

   def isEmpty(self):
       return len(self._data) == 0

# Dijkstra's - single source shortest path with non-negative weights
def dijkstra(graph, weights, source):
  min_heap = MyHeap([(source, 0)], key=lambda (v,w): w)
  while not min_heap.isEmpty():
    node, distance = min_heap.pop()
    if node not in shortest_distance:
      shortest_distance[node] = distance
      for neighbor in [n for n in graph[node] if n not in shortest_distance]:
        min_heap.push((neighbor, distance + weights[(node, neighbor)]))
  return shortest_distance



t = { "a" : ["b", "c", "d"],
      "b" : ["a", "e"],
      "c" : ["a"],
      "d" : ["a", "f", "g"],
      "e" : ["b"],
      "f" : ["d"],
      "g" : ["d"]
    }

g = { "a" : ["d"],
      "b" : ["c"],
      "c" : ["b", "c", "d", "e"],
      "d" : ["a", "c"],
      "e" : ["c"],
      "f" : []
    }

if __name__ == "__main__":
  BFS(g, "a")
  BFS(g, "b")
  BFS(g, "c")
  BFS(g, "d")
  BFS(g, "e")
  BFS(g, "f")

