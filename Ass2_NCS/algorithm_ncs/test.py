import sys
import argparse
parser = argparse.ArgumentParser(description="This is a NCS solver")
parser.add_argument("-c", "--config", default="algorithm_ncs/parameter.json", type=str, help="a json file that contains parameter")
parser.add_argument("-d", "--data", default="6", type=int, help="the problem dataset that need to be solved")
args = parser.parse_args()
config_file = args.config
p = args.data
print(config_file)
print(p)
print("test_case_1")
print(str(sys.argv))