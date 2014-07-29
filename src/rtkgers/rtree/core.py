"""
See class summary.

The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.7
@copyright 2014 - Present Aaron Zampaglione
"""
import abc

from rtkgers.kgers.original import KGERSOriginal

from rtkgers.rtree.node import Node


class RTreeCore(object):
  """
  The RTree core class contains methods that pertain to all recursive trees.
  """
  __metaclass__ = abc.ABCMeta


  def __init__(self, config, points):
    """
    Constructor.

    Key arguments:
    config -- The configuration to use.
    points -- The points to train on.
    """
    self.root = None
    self.config = config
    self.points = points

    # Determine the algorithm to use.
    self.algorithm = self.config.get('KGERS', 'Algorithm')

    # The minimum number of points necessary to run KGERS on.
    self.min_points = 3 * points[0].dimensions


  def error(self, test):
    """
    Determines the error based on the test set provided.

    Key arguments:
    test -- The test points to use
    """

    return math.sqrt(
      sum([pow(self.solve(point) - point.solution, 2) for point in test]) /
      float(len(test)))


  def hyperplane(self, point):
    """
    Returns the hyperplane to solve a point by recursively navigating the tree.

    Key arguments:
    point -- The point to analyze.
    """

    node = self.root
    while (node.left != None and node.right != None):
      if (point.features[node.feature] <= node.threshold):
        node = node.left
      else:
        node = node.right

    return node.hyperplane


  @abc.abstractmethod
  def grow(self, node, points):
    """
    The recursive method that builds the tree.
    """

    pass


  def populate(self):
    """
    Populates the tree by creating the root and calling the recursive
    abstract function.
    """

    self.root = Node()
    self.root.feature = None
    self.root.threshold = None
    self.root.hyperplane = globals()[self.algorithm](self.config, self.points)
    self.root.hyperplane.execute()

    self.grow(self.root, self.points)


  def solve(self, point):
    """
    Returns a solution for a point by recursively navigating the tree.

    Key arguments:
    point -- The point to analyze.
    """

    return self.hyperplane(point).solve(point)
