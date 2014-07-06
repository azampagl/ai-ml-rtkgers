"""
See class summary.

The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.7
@copyright 2014 - Present Aaron Zampaglione
"""
import numpy as np

from exceptions.hyperplane import HyperplaneException
from point import Point

class Hyperplane(object):
  """
  A n-dimensional subspace that was generated from a set of points.

  The coefficients represent the linear equation based on the points
  provided.
  """

  @staticmethod
  def factory(points):
    """
    Factory method that produces a hyperplane from points.

    Key arguments
    points -- The points to a build a hyperplane from.
    """

    # Make sure we have the minimum number of points necessary.
    if len(points) > 0 and len(points) < points[0].dimensions:
      raise HyperplaneException(
        "Not enough points to make a hyperplane in this dimension."
      )

    # Make sure we are provided with a full rank matrix.
    points_as_array = np.array(
      [point.coordinates for point in points],
      dtype=Point.DTYPE
      )

    if round(np.linalg.det(points_as_array), 1) == 0.0:
      raise HyperplaneException("The points provided are linearly dependent.")

    # Build our linear equation matrix
    a = np.array(
      [np.append(point.features, [1.0]) for point in points],
      dtype=Point.DTYPE
      )

    b = np.array(
      [point.solution for point in points],
      dtype=Point.DTYPE
      )

    return Hyperplane(np.linalg.solve(a, b))


  def __init__(self, coefficients):
    """
    Constructor.

    Key arguments
    coefficients -- The coefficients of the linear equation for the hyperplane.
    """

    self.coefficients = coefficients


  def solve(self, point):
    """
    Given a point (set of features), return the predicted solution.

    E.g.

      The hyperplane has coefficients [3.0, 2.0, 1.0] (3.0x + 2.0y + 1.0).

      A point with values [4.0, 5.0] (x, y) is provided.

      solve(Point([4.0, 5.0])) =>

        (3.0 x 4.0) + (2.0 x 5.0) + 1.0 => 23.0

    """

    return sum([a * b for a, b in zip(self.coefficients[:-1], point.features)]) \
      + self.coefficients[-1]
