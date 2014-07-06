"""
See class summary.

The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.7
@copyright 2014 - Present Aaron Zampaglione
"""
import numpy as np

class Point(object):
  """
  A point represents a feature set and the solution.

  For example, let assume we have a three-dimensional "Point", (x, y, z).

  The feature set would be [x, y] and the solution would be z (the items we
  are trying to predict).

  point = Point([x, y], z)
  point.features = [x, y]
  point.solution = z
  """

  # The data type for the coordinates of a point.
  DTYPE = np.dtype(float)


  def __init__(self, features, solution = None):
    """
    Constructor.

    Key arguments
    features -- The features for this point.
                For example, if we a three-dimensional point, (x, y, z),
                the features would be "[x, y]".
    solution -- The solution for this point.
                For example, if this was a three-dimensional point, (x, y, z),
                the solution would be "z".
    """

    # The coordinates are the features plus the solution as the last element.
    coordinates = list(features) + [solution]

    # Copy over the original features set.
    self.coordinates = np.array(coordinates, dtype=Point.DTYPE)

    # Find the dimensions of the point.
    self.dimensions = len(self.coordinates)


  def __str__(self):
    """Return a string representation."""

    return "(" + ", ".join(str(x) for x in self.coordinates) + ")"


  @property
  def features(self):
    """Return the feature set."""

    return self.coordinates[:-1]


  @property
  def solution(self):
    """Gets the solution."""

    return self.coordinates[-1]


  @solution.setter
  def solution(self, value):
    """Sets the solution."""

    self.coordinates[-1] = value
