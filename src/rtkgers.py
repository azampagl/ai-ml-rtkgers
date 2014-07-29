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

import ConfigParser

from rtkgers.point import Point
from rtkgers.rtree.original import RTreeOriginal


# The mode when execution is for "training".
MODE_TRAIN = 'train'


# The mode when execution is for "predicting".
MODE_PREDICT = 'predict'


def main():
  """Main execution."""

  # Determine command line arguments.
  try:
    rawopts, _ = getopt.getopt(sys.argv[1:], 'c:e:m:i:o:')
  except getopt.GetoptError:
    usage()
    sys.exit(2)

  opts = {}

  # Process each command line argument.
  for o, a in rawopts:
    opts[o[1]] = a

  # The following arguments are required in all cases.
  for opt in ['e', 'i', 'o']:
    if not opt in opts:
      usage()
      sys.exit(2)

  # Training.
  if opts['e'] == MODE_TRAIN:
    # Make sure the config was provided.
    if not 'c' in opts:
      usage()
      sys.exit(2)

    train(opts['c'], opts['i'], opts['o'])

  # Prediction.
  elif opts['e'] == MODE_PREDICT:
    # Make sure the model was provided.
    if not 'm' in opts:
      usage()
      sys.exit(2)

    predict(opts['m'], opts['i'], opts['o'])

  # Mode not recognized.
  else:
    usage()
    sys.exit(2)


def predict(model_filename, input_filename, output_filename):
  """
  Loads in a rtkgers model and predicts the values in the input file.

  Key arguments:
  model_filename  -- The rtkgers model written to disk.
  input_filename  -- The input file name with the test values.
  output_filename -- The output file for the prediction values.
  """

  with open(model_filename, 'rb') as model_file:
    rtkgers = pickle.load(model_file)

  # Create our reader.
  with open(input_filename, 'rb') as reader_file:
    reader = csv.reader(reader_file, delimiter=',', quotechar='|')
    with open(output_filename, 'wb') as writer_file:
      writer = csv.writer(writer_file, delimiter=',', quotechar='|')

      # Skip the first line.
      reader.next()
      for row in reader:
        point = Point([float(feature) for feature in row[2:]])
        solution = rtkgers.solve(point)
        writer.writerow([row[0]] + [solution] + row[2:])


def train(config_filename, input_filename, output_filename):
  """
  Generates a RTKGERS model based on the provided training set and config.

  Key arguments:
  config_filename  -- The config file name.
  input_filename   -- The input file name.
  output_filename  -- The output file name.
  """

  # Load in the configuration.
  config = ConfigParser.ConfigParser()
  config.read(config_filename)

  # The points are essentially feature sets with the known solution.
  points = []

  # Create our reader.
  with open(input_filename, 'rb') as reader_file:
    reader = csv.reader(reader_file, delimiter=',', quotechar='|')

    # Skip the first line.
    reader.next()
    for row in reader:
      points.append(
        Point([float(feature) for feature in row[2:]], float(row[1])))

  # Load the desired algorithm.
  algorithm = config.get('RTree', 'Algorithm')
  rtkgers = globals()[algorithm](config, points)

  # Execute.
  rtkgers.populate()

  with open(output_filename, 'wb') as output_file:
    pickle.dump(rtkgers, output_file, pickle.HIGHEST_PROTOCOL)


def usage():
  """Prints the usage of the program."""

  print("\n" +
    "The following are arguments required:\n" +
    "\t-c: the path to the configuration file.\n" +
    "\t-e: the execution mode (train,predict).\n" +
    "\t-m: the model file (only required in predict mode).\n" +
    "\t-i: the input file.\n" +
    "\t-o: the output file.\n" +
    "\n" +
    "Example Usage:\n" +
    "\tpython rtkgers.py -e \"train\" -c \"config.cfg\" -i \"training.csv\" -o \"rtkgers.model\"\n" +
    "\tpython rtkgers.py -e \"predict\" -m \"rtkgers.model\" -i \"test.csv\" -o \"predictions.csv\"" +
    "\n")


"""Main execution."""
if __name__ == "__main__":
  main()
