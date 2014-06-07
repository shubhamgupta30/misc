""" Class to represent a solution generated when relod action is received
"""
class Solution(object):

  """ Initializes a solution.
  Args:
    displayed_stories: the stories displayed by this solution
    stories_considered: candisate stories considered by this solution
  """
  def __init__(self):
    self.displayed_stories = []
    self.stories_considered = []

""" A class to represent attributes of a story
"""
class Story(object):
  """ __count indicates the number of stories creayted so far
  """
  __count = 0

  """ Initialize a story
  Args:
    time: time at which the story appears
    score: the score of this story
    height: the height of this story
  """
  def __init__(self, time, score, height):
    self.time = time
    self.score = score
    self.height = height
    Story.__count += 1
    self.id = Story.__count

""" Class that perfoms the feed optimization
"""
class FeedOptimizer(object):

  """ Initializes an  feed optimizer
  Args:
    time_window: Time window in which stories are to be considered
    browser_height: height of the browser
  """
  def __init__(self, time_window, browser_height):
    self._stories = []
    self._last_solution = Solution()
    self._time_window = time_window
    self._browser_height = browser_height
    """ Knapsack table we are going to use always.
    knapsack_table[i][j] considers the problem when we consider only first i
    items with browser height as j. We store the following information at
    this location (in this order):
      score: max score possible in this scenario
      num_stories: number of stories displayed to achieve this
      include_i: is the story corresponding to this row displayed
    Creating big enough table using bounds given in the problem
    """
    self._knapsack_table = []

  """ Adds a newly published story to the optmizer
  Args:
    story: object of class Story representing the new story received
  """
  def add_story(self, story):
    # Do not add story if it is too big to be used anyways
    if story.height <= self._browser_height:
      self._stories.append(story)

  """ Computes the stories to display when a reload request is received
  Args:
    time: Time at which the request arrives
  """
  def handle_reload(self, time):
    # The stories that must be considered for displaying on browser screen
    # These are ordered in decreasing order of arrival time, i.e. newest
    # items are at the top.
    stories_to_consider = [
        s for s in self._stories if s.time + self._time_window >= time][::-1]
    self._knapsack_table = [[
      (0, 0, False) for h in xrange(self._browser_height+1)]
      for s in xrange(len(stories_to_consider))]

    # Do we have any stories to consider?
    if not stories_to_consider:
      self._last_solution.displayed_stories = []
      self._last_solution.stories_considered = []
      self._print_solution()
      return

    # Did we compute our last solution on exactly these stories?
    if self._last_solution.stories_considered == stories_to_consider:
      self._print_solution()
      return

    # Solve the 0-1 knapsack problem
    #
    # Initialize
    for h in xrange(self._browser_height + 1):
      if h < stories_to_consider[0].height:
        self._knapsack_table[0][h] = (0, 0, False)
      else:
        self._knapsack_table[0][h] = (stories_to_consider[0].score, 1, True)


    # Perform the recursion phase
    for s in xrange(1, len(stories_to_consider)):
      for h in xrange(self._browser_height + 1):
        story = stories_to_consider[s]
        if self._use_story(story, (s,h)):
          (score, num_stories, use_story) = self._knapsack_table[s-1][h-story.height]
          self._knapsack_table[s][h] = (score + story.score, num_stories+1, True)
        else:
          (score, num_stories, use_story) = self._knapsack_table[s-1][h]
          self._knapsack_table[s][h] = (score, num_stories, False)

    # Generate Solution
    self._compute_solution(stories_to_consider)
    self._print_solution()
    return

  """ Decides if we should include story i in the solution computed for a
  particular cell of the knapsack table
  Args:
    story: the story under consideration
    (s,h): (int, int) - the location in the knapsack table being filled
  """
  def _use_story(self, story, (s,h)):
    if h < story.height:
      return False
    without_story = self._knapsack_table[s-1][h]
    with_story = self._knapsack_table[s-1][h-story.height]
    if without_story[0] < with_story[0] + story.score:
      return True
    return (without_story[0] == with_story[0] + story.score) and (
        without_story[1] >= with_story[1] + 1)

  """ Computes the solution from the knapsack table
  Args:
    stories_to_consider: The list f stories considered for this knapsack
  """
  def _compute_solution(self, stories_to_consider):
    displayed_stories = []
    row = len(stories_to_consider)-1
    column = self._browser_height
    while row >=0 and column >= 0:
      if self. _knapsack_table[row][column][2]:
        displayed_stories.append(stories_to_consider[row])
        column -= stories_to_consider[row].height
      row -= 1
    self._last_solution.displayed_stories = displayed_stories
    self._last_solution.stories_considered = stories_to_consider

  """ Displays the solution in the required format
  """
  def _print_solution(self):
    max_score = sum([story.score for story in self._last_solution.displayed_stories])
    num_stories = len(self._last_solution.displayed_stories)
    stories = " ".join([str(story.id) for story in self._last_solution.displayed_stories])
    print "%d %d %s"%(max_score, num_stories, stories)



def main():
  [N, W, H] = [int(n) for n in raw_input().split(" ")]
  feed_optimizer = FeedOptimizer(W, H)
  while N > 0:
    input_str = raw_input()
    if input_str.startswith("S"):
      [time, score, height] = [int(n) for n in input_str[2:].split(" ")]
      feed_optimizer.add_story(Story(time, score, height))
    else:
      time = int(input_str[2:])
      feed_optimizer.handle_reload(time)
    N -= 1


if __name__ == "__main__":
  main()
