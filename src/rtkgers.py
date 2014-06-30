"""
Main execution script.

The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.7
@copyright 2014 - Present Aaron Zampaglione
"""
import ConfigParser
import getopt
import os
import sys

from rtkgers.point import Point
from rtkgers.hyperplane import Hyperplane

def main():
  """Main execution."""

  # Determine command line arguments.
  try:
    rawopts, _ = getopt.getopt(sys.argv[1:], 'c:')
  except getopt.GetoptError:
    usage()
    sys.exit(2)

  opts = {}

  # Process each command line argument.
  for o, a in rawopts:
    opts[o[1]] = a

  # The following arguments are required in all cases.
  for opt in ['c']:
    if not opt in opts:
      usage()
      sys.exit(2)

  # Load in the configuration.
  config = ConfigParser.ConfigParser()
  config.read(opts['c'])

  points = []
  points.append(Point([1.0], 3.0))
  points.append(Point([3.0], 7.0))

  hyperplane = Hyperplane(points)

  print(hyperplane.coefficients)


def usage():
  """Prints the usage of the program."""

  print("\n" +
    "The following are arguments required:\n" +
    "\t-c: the path to the configuration file.\n" +
    "\n" +
    "Example Usage:\n" +
    "\tpython rtkgers.py -c \"config.cfg\"" +
    "\n")


"""Main execution."""
if __name__ == "__main__":
  main()
