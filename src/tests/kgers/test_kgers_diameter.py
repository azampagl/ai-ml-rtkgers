"""
Test the KGERS algorithm with weights.

The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.7
@copyright 2014 - Present Aaron Zampaglione
"""
import ConfigParser
import numpy as np
import pytest

from rtkgers.hyperplane import Hyperplane
from rtkgers.point import Point
from rtkgers.kgers.diameter import KGERSDiameter

from rtkgers.exceptions.hyperplane import HyperplaneException


def config():
  """Returns the default configuration to use for the KGERS algorithm."""

  config = ConfigParser.RawConfigParser()

  config.add_section('Main')
  config.set('Main', 'MaxThreads', 4)

  config.add_section('KGERS')
  config.set('KGERS', 'K', 10)

  config.add_section('KGERSDiameter')
  config.set('KGERSDiameter', 'Multiple', 2)

  Hyperplane.MAX_SAMPLE_ATTEMPTS = 200

  return config


def test_kgers_perfect():
  """Test kgers with points that form a perfect linear equation."""

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

  kgers = KGERSDiameter(config(), points)
  kgers.execute()

  assert np.all([kgers.coefficients, [3.0, 2.0, 2.0]])


def test_kgers_fail():
  """Test kgers with points that will not sucessfully make a hyperplane."""

  # Make nine points identical so a hyperplane cannot be formed.
  points = []
  points.append(Point([2.0, 2.0], 12.0))
  points.append(Point([2.0, 2.0], 12.0))
  points.append(Point([2.0, 2.0], 12.0))
  points.append(Point([2.0, 2.0], 12.0))
  points.append(Point([2.0, 2.0], 12.0))
  points.append(Point([2.0, 2.0], 12.0))
  points.append(Point([2.0, 2.0], 12.0))
  points.append(Point([2.0, 2.0], 12.0))
  points.append(Point([2.0, 2.0], 12.0))

  kgers = KGERSDiameter(config(), points)

  with pytest.raises(HyperplaneException):
    kgers.execute()
