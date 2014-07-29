"""
Test the original KGERS algorithms.

The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.7
@copyright 2014 - Present Aaron Zampaglione
"""
import ConfigParser
import numpy as np
import pytest

from rtkgers.point import Point
from rtkgers.rtree.original import RTreeOriginal


def config():
  """Returns the default configuration to use for the RTree algorithm."""

  config = ConfigParser.RawConfigParser()

  config.add_section('Main')
  config.set('Main', 'MaxThreads', 4)

  config.add_section('KGERS')
  config.set('KGERS', 'Algorithm', 'KGERSOriginal')
  config.set('KGERS', 'K', 10)

  return config


def test_simple_line_perfect():
  """Tests the recursive tree using a perfect line."""

  # Make nine points for a three dimensional
  #  space for equation 3x + 2y + 2 = z
  points = []
  points.append(Point([2.0, 2.0], 12.0))
  points.append(Point([3.0, 4.0], 19.0))
  points.append(Point([4.0, 5.0], 24.0))
  points.append(Point([5.0, 6.0], 29.0))
  points.append(Point([6.0, 7.0], 34.0))
  points.append(Point([7.0, 8.0], 39.0))
  points.append(Point([8.0, 9.0], 44.0))
  points.append(Point([9.0, 10.0], 49.0))
  points.append(Point([10.0, 11.0], 54.0))
  points.append(Point([11.0, 12.0], 59.0))

  rtkgers = RTreeOriginal(config(), points)
  rtkgers.populate()

  # Assert that only one node was made since it was a perfect line.
  assert rtkgers.root.left == None
  assert rtkgers.root.right == None
  # Make sure the solution is within range.
  solution = rtkgers.solve(Point([7.0, 8.0]))
  assert solution >= 37.0 and solution <= 41.0


def test_two_lines_perfect():
  """Tests the recursive tree using two perfect line."""

  # Make nine points for a three dimensional
  #  space for equation 3x + 2y + 2 = z
  points = []
  points.append(Point([2.0, 2.0], 12.0))
  points.append(Point([3.0, 4.0], 19.0))
  points.append(Point([4.0, 5.0], 24.0))
  points.append(Point([5.0, 6.0], 29.0))
  points.append(Point([6.0, 7.0], 34.0))
  points.append(Point([7.0, 8.0], 39.0))
  points.append(Point([8.0, 9.0], 44.0))
  points.append(Point([9.0, 10.0], 49.0))
  points.append(Point([10.0, 11.0], 54.0))
  points.append(Point([11.0, 12.0], 59.0))

  # Make nine points for a three dimensional
  #  space for equation 2x + y + 20 = z
  points.append(Point([22.0, 22.0], 86.0))
  points.append(Point([23.0, 24.0], 90.0))
  points.append(Point([24.0, 25.0], 93.0))
  points.append(Point([25.0, 26.0], 96.0))
  points.append(Point([26.0, 27.0], 99.0))
  points.append(Point([27.0, 28.0], 102.0))
  points.append(Point([28.0, 29.0], 105.0))
  points.append(Point([29.0, 30.0], 108.0))
  points.append(Point([30.0, 31.0], 111.0))

  rtkgers = RTreeOriginal(config(), points)
  rtkgers.populate()

  node1 = rtkgers.root.left
  node2 = rtkgers.root.right

  # There is a possibility that no split occurred because of randomization...
  #  which we can't really unit test for. Only evaluate if we can check
  #  the right and left nodes.
  if node1 != None and node2 != None:

    # Check that the left node is the last leaf on the left.
    assert node1 != None
    assert node1.left == None
    assert node1.right == None
    # Make sure the solution is within range.
    solution = rtkgers.solve(Point([7.0, 8.0]))
    assert solution >= 37.0 and solution <= 41.0

    # Check that the right node is the last leaf on the right.
    assert node2 != None
    assert node2.left == None
    assert node2.right == None
    # Make sure the solution is within range.
    solution = rtkgers.solve(Point([28.0, 29.0]))
    assert solution >= 103.0 and solution <= 107.0
