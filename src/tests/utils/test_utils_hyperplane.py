"""
Test the hyperplane utility methods.

The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.7
@copyright 2014 - Present Aaron Zampaglione
"""
import numpy as np
import sys

from rtkgers.point import Point
from rtkgers.hyperplane import Hyperplane

from rtkgers.utils.hyperplane import average
from rtkgers.utils.hyperplane import weigh

def test_average():
  """Test the average method with a typical example."""

  weights = []
  hyperplanes = []

  weights.append(100.0)
  hyperplanes.append(Hyperplane(np.array([2.0, 1.0], dtype=Point.DTYPE), []))

  weights.append(100.0)
  hyperplanes.append(Hyperplane(np.array([3.0, 2.0], dtype=Point.DTYPE), []))

  assert np.all([average(hyperplanes, weights), [2.5, 1.5]])


def test_average_perfect():
  """Test averaging with one perfect hyperplane in the list."""

  weights = []
  hyperplanes = []

  weights.append(sys.float_info.max)
  hyperplanes.append(Hyperplane(np.array([2.0, 1.0], dtype=Point.DTYPE), []))

  weights.append(100.0)
  hyperplanes.append(Hyperplane(np.array([3.0, 2.0], dtype=Point.DTYPE), []))

  assert np.all([average(hyperplanes, weights), [2.0, 1.0]])

def test_weigh_perfect():
  """Test the weigh method with a perfect hyperplane."""

  validators = []
  validators.append(Point([3.0], 7.0))

  hyperplane = Hyperplane(np.array([2.0, 1.0], dtype=Point.DTYPE), [])

  assert weigh(hyperplane, validators) == sys.float_info.max


def test_weigh_nonperfect():
  """Test the weigh method with a validator that is slightly off."""

  validators = []
  validators.append(Point([3.0], 6.9))

  hyperplane = Hyperplane(np.array([2.0, 1.0], dtype=Point.DTYPE), [])

  # Since the validator is 0.1 off from the actual (7.0 - 6.9), after the
  #  square error is found (0.01), we return what fraction of one that is.
  #  e.g. 1.0 / 0.01 == 100
  assert round(weigh(hyperplane, validators)) == 100.0
