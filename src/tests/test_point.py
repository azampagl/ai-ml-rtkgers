"""
Test the point class.

The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.7
@copyright 2014 - Present Aaron Zampaglione
"""
from rtkgers.point import Point


def test_point_default():
  """Test a point class with no solution."""

  # Make a point.
  point = Point([1, 2])

  assert point.coordinates == [1, 2, None]
  assert point.features == [1, 2]
  assert point.solution == None


def test_point_with_solution():
  """Test a point with a solution."""

  # Make a point with a solution.
  point = Point([1, 2], 3)

  assert point.coordinates == [1, 2, 3]
  assert point.features == [1, 2]
  assert point.solution == 3


def test_point_set_solution():
  """Test getting and settings the solution on a point."""

  # Make a point.
  point = Point([1, 2], 3)

  assert point.solution == 3

  # Try setting a solution.
  point.solution = 4

  assert point.solution == 4
  assert point.coordinates == [1, 2, 4]
