class FeedOptimizer(object):

  class Story(object):
    def __init__(self, publication_time, score, height, index):
      self.publication_time = publication_time
      self.score = score
      self.height = height
      self.index = index

  class SolutionState(object):
    def __init__(self):
      self.max_score = 0
      self.displayed_stories = []
      self.start_index_in_stories = 0 
      self.len_stories = 0
      self.knapsack_DP_table = {}
      self.stories_counts_table = {}
      self.story_use_table = {}

  def __init__(self, browser_height, time_window):
    self._browser_height = browser_height
    self._time_window = time_window
    self._next_story_index = 1
    self._solution = self.SolutionState()
    self._stories = []

  def add_story_event(self, publication_time, score, height):
    self._stories.append(self.Story(publication_time, score, height, self._next_story_index))
    self._next_story_index += 1

  def story_change_since_last_reload(self, timestamp):
    index = self._solution.start_index_in_stories
    while index < len(self._stories) and self._stories[index].publication_time + self._time_window < timestamp:
      index += 1
    return index

  def recompute_table(self, start_index_in_stories):
    # knapsack_DP_table[(i,j)] represents the maximum score we can display
    # using first i stories and if the browser height is j.
    knapsack_DP_table = {}
    # stories_counts_table[(i,j)] represents the number of stories in the
    # solution that displays maximum possible score on the screen, using first
    # i stories on a browser of height j. This is used for tie breaking
    stories_counts_table = {}
    # story_use_table[(i,j)] = True if we used story i in deciding score at
    # knapsack_DP_table[(i,j)]
    story_use_table = {}
    # stories are ordered in decreasing order of timestamp. This is useful for
    # tie breaking
    stories = self._stories[start_index_in_stories:][::-1]

    # Initialize
    for h in xrange(self._browser_height + 1):
      if h < stories[0].height :
        knapsack_DP_table[(0, h)] = 0
        stories_counts_table[(0, h)] = 0
        story_use_table[(0,h)] = False
      else :
        knapsack_DP_table[(0, h)] = stories[0].score
        stories_counts_table[(0, h)] = 1
        story_use_table[(0,h)] = True

    # Fill the rest of the table
    for i in xrange(1, len(stories)):
      for j in xrange(self._browser_height + 1):
        story_height = stories[i].height
        score_without_i = knapsack_DP_table[(i-1, j)]
        stories_without_i = stories_counts_table[(i-1,j)]
        (score, num_stories, used_story_i) = (0, 0, False)
        if story_height > j:
          (score, num_stories, used_story_i) = (score_without_i, stories_without_i, False)
        else:
          score_with_i = knapsack_DP_table[(i-1, j-story_height)] + stories[i].score
          stories_with_i = stories_counts_table[(i-1, j-story_height)] + 1
          if score_with_i < score_without_i or (
              score_with_i == score_without_i and stories_without_i < stories_with_i):
            (score, num_stories, used_story_i) = (score_without_i, stories_without_i, False)
          else:
            (score, num_stories, used_story_i) = (score_with_i, stories_with_i, True)

        # Assign
        knapsack_DP_table[(i,j)] = score
        stories_counts_table[(i,j)] = num_stories
        story_use_table[(i,j)] = used_story_i

    # Compute the Solution
    self._solution.knapsack_DP_table = knapsack_DP_table
    self._solution.stories_counts_table = stories_counts_table
    self._solution.story_use_table = story_use_table
    self.compute_stories_to_display(stories)

  def calculate_solution_from_existing_table(self, new_index):
    self.compute_stories_to_display(self._stories[new_index:][::-1])

  def compute_stories_to_display(self, stories):
    row = len(stories) - 1
    column = self._browser_height
    self._solution.max_score = self._solution.knapsack_DP_table[(row, column)]
    self._solution.displayed_stories = []
    while row >= 0 and column >= 0:
      if self._solution.story_use_table[(row, column)]:
        self._solution.displayed_stories.append(stories[row].index)
        column -= stories[row].height
      row -= 1


  def handle_reload(self, timestamp):
    new_start_index_in_stories = self.story_change_since_last_reload(timestamp)
    num_stories_added = len(self._stories) - self._solution.len_stories
    num_stories_discarded = new_start_index_in_stories - self._solution.start_index_in_stories
    self._solution.len_stories = len(self._stories)
    self._solution.start_index_in_stories = new_start_index_in_stories

    # No change since last reload. Display previously computed solution.
    if num_stories_added == 0 and num_stories_discarded == 0:
      self.printSolution()
      return
    # No stories to show
    if new_start_index_in_stories == len(self._stories):
      self._solution = self.SolutionState()
      self.printSolution()
      return
    # No stories added since last reload. We can compute new solution from
    # existing DP table
    if num_stories_added == 0:
      self.calculate_solution_from_existing_table(new_start_index_in_stories)
      self.printSolution()
      return
    self.recompute_table(new_start_index_in_stories)
    self.printSolution()

  def printSolution(self):
    print "%d %d %s" % (self._solution.max_score, len(self._solution.displayed_stories),
        " ".join([str(s) for s in self._solution.displayed_stories]))


def main():
  (N, W, H) = [int(n) for n in raw_input().split(" ")]
  feed_optimizer = FeedOptimizer(H, W)
  while N > 0:
    input_str = raw_input()
    if input_str.startswith("S"):
      [time, score, height] = [int(n) for n in input_str[2:].split(" ")]
      feed_optimizer.add_story_event(time, score, height)
    else:
      timestamp = int(input_str[2:])
      feed_optimizer.handle_reload(timestamp)
    N -= 1

if __name__ == "__main__":
  main()
