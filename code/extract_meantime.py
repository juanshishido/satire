#usage: python extract_meantime.py <input_path> <output_path>
#example usage: python meantime meantime_data

import sys
from os import listdir
from os.path import isfile, join


def extract_raw(s):
	return s.split("<raw>")[1].split("</raw>")[0]

input_path = sys.argv[1]
output_path = sys.argv[2] + "/"

inputs = [f for f in listdir(input_path) if isfile(join(input_path, f)) and ".naf" in f]
for f in inputs:
	output_filename = f.split(".naf")[0] + ".txt"
	content = open(f).read()
	output_file = open(output_path + output_filename, 'w')
	output_file.write(extract_raw(content))
	output_file.close()
