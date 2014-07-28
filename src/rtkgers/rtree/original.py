"""
The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.7
@copyright 2013 - Present Aaron Zampaglione
"""
from rtkgers.exceptions.hyperplane import HyperplaneException
from rtkgers.kgers.original import KGERSOriginal
from rtkgers.rtree.node import Node
from rtkgers.rtree.core import RTreeCore

class RTreeOriginal(RTreeCore):
  """
  Grows the recursive tree by analyzing every point and every feature
  possible to determine the best split.
  """

  def grow(self, node, points):
    """See parent."""

    node.points = points

    # Return if we do not have enough points to split.
    if (len(points) < self.min_points * 2):
      return

    # Keep track of the best index / node to split at.
    best_index = None
    best_feature = None
    best_left = None
    best_right = None
    best_error = node.hyperplane.error()

    for f in range(len(points[0].features)):
      # Sort the points by the feature provided.
      points = sorted(points, key=lambda x: x.features[f])
      # Cycle through every point evaluating at the desired feature.
      for i in range(self.min_points, len(points) - self.min_points + 1):

        left_points = points[:i]
        right_points = points[i:]

        left = globals()[self.algorithm](self.config, left_points)
        right = globals()[self.algorithm](self.config, right_points)

        # Try to generate a hyperplane.
        try:
          left.execute()
          right.execute()
        except HyperplaneException, e:
          continue

        error = (len(left_points) / float(len(points))) * left.error() + \
          (len(right_points) / float(len(points))) * right.error()

        print str(best_error) + " - " + str(error)
        if (best_error > error):
          best_index = i
          best_feature = f
          best_error = error
          best_left = left
          best_right = right

    if (best_index != None):
      node.feature = best_feature
      node.threshold = points[best_index].features[best_feature]

      node.left = Node()
      node.left.hyperplane = best_left

      self.grow(node.left, points[:best_index])

      node.right = Node()
      node.right.hyperplane = best_right
      self.grow(node.right, points[best_index:])
