"""
Main execution script.

The style guide follows the strict python PEP 8 guidelines.
@see http://www.python.org/dev/peps/pep-0008/

@author Aaron Zampaglione <azampagl@azampagl.com>
@requires Python >=2.7
@copyright 2014 - Present Aaron Zampaglione
"""
import csv
import getopt
import os
import pickle
import sys
import tempfile
import uuid

import matplotlib.pyplot as plot

from rtkgers.point import Point
from rtkgers.rtree.original import RTreeOriginal

def main():
  """Main execution."""

  # Determine command line arguments.
  try:
    rawopts, _ = getopt.getopt(sys.argv[1:], 'c:i:')
  except getopt.GetoptError:
    usage()
    sys.exit(2)

  opts = {}

  # Process each command line argument.
  for o, a in rawopts:
    opts[o[1]] = a

  # The following arguments are required in all cases.
  for opt in ['c', 'i']:
    if not opt in opts:
      usage()
      sys.exit(2)

  # Read in all the points we wish to plot.
  points = []
  with open(opts['i'], 'rb') as reader_file:
    reader = csv.reader(reader_file, delimiter=',', quotechar='|')

    # Skip the first line
    reader.next()
    for row in reader:
      points.append(Point([float(feature) for feature in row[2:]], float(row[1])))

  # Find the max coordinates.
  max_x = max([point.coordinates[0] for point in points])
  max_y = max([point.coordinates[1] for point in points])
  min_x = min([point.coordinates[0] for point in points])
  min_y = min([point.coordinates[1] for point in points])
  plot.axis([min(min_x, 0.0) - 1, max(max_x, 10.0) + 1, min(min_y, 0.0) - 1, max(max_y, 10.0) + 1])

  # Draw all the points.
  figure = 1
  plot.figure(figure)
  plot.plot(
      [point.coordinates[0] for point in points],
      [point.coordinates[1] for point in points],
      'ko'
  )

  model_filename = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))

  os.system("python ../src/rtkgers.py " +
            "-e train " +
            "-c " + opts['c'] + " " +
            "-i demo-2d-simple.csv " +
            "-o " + model_filename)

  with open(model_filename, 'rb') as model_file:
    # Load in the model.
    rtkgers = pickle.load(model_file)

    # For every point, find the corresponding hyperplane.
    hyperplanes = {}
    for point in points:
      hyperplane = rtkgers.hyperplane(point)
      if not hyperplane in hyperplanes:
        hyperplanes[hyperplane] = []
      hyperplanes[hyperplane].append(point)

  for hyperplane,points in hyperplanes.iteritems():
    max_point = reduce(
      lambda point1, point2:
        point1 if point1.coordinates[0] > point2.coordinates[0] else point2,
        points[1:], points[0])
    min_point = reduce(
      lambda point1, point2:
        point1 if point1.coordinates[0] < point2.coordinates[0] else point2,
        points[1:], points[0])

    plot.plot(
      [min_point.coordinates[0], max_point.coordinates[0]],
      [hyperplane.solve(min_point), hyperplane.solve(max_point)],
      'r-'
    )

  os.remove(model_filename)

  # Show the plot.
  plot.show()


def usage():
  """Prints the usage of the program."""

  print("\n" +
    "The following are arguments required:\n" +
    "\t-i: the input file.\n" +
    "\t-i: the input file.\n" +
    "\n" +
    "Example Usage:\n" +
    "\tpython demo.py -c \"defaults.cfg\" -i \"input.csv\"" +
    "\n")


"""Main execution."""
if __name__ == "__main__":
  main()
