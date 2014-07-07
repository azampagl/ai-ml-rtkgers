"""
Test the point class.

The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.7
@copyright 2014 - Present Aaron Zampaglione
"""
import pytest

from rtkgers.point import Point
from rtkgers.hyperplane import Hyperplane

from rtkgers.exceptions.hyperplane import HyperplaneException


def test_hyperplane_simple():
  """Test creating a simple hyperplane."""

  # Make two points to create a simple hyperplane
  #  for equation 2x + 1
  points = []
  points.append(Point([1.0], 3.0))
  points.append(Point([3.0], 7.0))

  hyperplane = Hyperplane.factory(points)

  # Round the coefficients to the nearest decimal.
  rounded_coefficients = \
    [round(coefficient) for coefficient in hyperplane.coefficients]

  assert rounded_coefficients == [2.0, 1.0]

  # 2(5) + 1 = 11
  assert round(hyperplane.solve(Point([5.0]))) == 11.0


def test_hyperplane_insufficient_points():
  """Test creating a simple hyperplane."""

  # Make two points for a three dimensional
  #  space, which should throw an exception.
  points = []
  points.append(Point([1.0, 2.0], 1.0))
  points.append(Point([2.0, 2.0], 2.0))

  assert points[0].dimensions == 3

  with pytest.raises(HyperplaneException):
    hyperplane = Hyperplane.factory(points)


def test_hyperplane_linearly_dependent():
  """Test creating a hyperplane with linearly dependent points."""

  # Make two points for a three dimensional
  #  space, which should throw an exception.
  points = []
  points.append(Point([1.0, 1.0], 1.0))
  points.append(Point([2.0, 2.0], 2.0))
  points.append(Point([3.0, 3.0], 3.0))

  assert points[0].dimensions == 3

  with pytest.raises(HyperplaneException):
    hyperplane = Hyperplane.factory(points)


def test_hyperplane_sample_fail():
  """
  Test failing to create a hyperplane with a
  large set of linearly dependent points.
  """

  # Make a large amount of points for a three dimensional
  #  space, which should throw an exception since they are all linearly
  #  dependent.
  points = []
  points.append(Point([1.0, 1.0], 1.0))
  points.append(Point([2.0, 2.0], 2.0))
  points.append(Point([3.0, 3.0], 3.0))
  points.append(Point([4.0, 4.0], 4.0))
  points.append(Point([5.0, 5.0], 5.0))
  points.append(Point([6.0, 6.0], 6.0))
  points.append(Point([7.0, 7.0], 7.0))

  with pytest.raises(HyperplaneException):
    hyperplane = Hyperplane.sample(points)

def test_hyperplane_sample_success():
  """
  Test sample a bunch of points to generate a
  three dimensional hyperplane.
  """

  # Make a few points for a three dimensional
  #  space for equation 3x + 2y + 2 = z
  points = []
  points.append(Point([2.0, 2.0], 12.0))
  points.append(Point([3.0, 4.0], 19.0))
  points.append(Point([4.0, 5.0], 24.0))
  points.append(Point([6.0, 7.0], 36.0))

  hyperplane = Hyperplane.sample(points)

  assert hyperplane.coefficients.dtype.type is Point.DTYPE.type

  # 3(5) + 2(6) + 2 = 29, or approximately.
  #  One of the hyperplanes generated returns a result of ~30.5
  solution = hyperplane.solve(Point([5.0, 6.0]))
  assert solution >= 28.0 and solution <= 31.0


def test_hyperplane_three_dimensional():
  """Test creating a three dimensional hyperplane."""

  # Make three points for a three dimensional
  #  space for equation 3x + 2y + 2 = z
  points = []
  points.append(Point([2.0, 2.0], 12.0))
  points.append(Point([3.0, 4.0], 19.0))
  points.append(Point([4.0, 5.0], 24.0))

  hyperplane = Hyperplane.factory(points)

  # Round the coefficients to the nearest decimal.
  rounded_coefficients = \
    [round(coefficient) for coefficient in hyperplane.coefficients]

  assert hyperplane.coefficients.dtype.type is Point.DTYPE.type
  assert rounded_coefficients == [3.0, 2.0, 2.0]

  # 3(5) + 2(6) + 2 = 29
  assert round(hyperplane.solve(Point([5.0, 6.0]))) == 29.0
