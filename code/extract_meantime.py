#script to parse news articles (available at http://www.newsreader-project.eu/results/data/) in the NAF format
#usage: python extract_meantime.py <input_path> <output_path>
#example usage: python meantime meantime_data

import sys
from os import listdir
from os.path import isfile, join
import bz2

def extract_raw(s):
    result = s.split("<raw>")[1].split("</raw>")[0]
    if "![CDATA[" in result:
        result = result.split("![CDATA[")[1].split("]]>")[0]
    return result

input_path = sys.argv[1]
output_path = sys.argv[2] + "/"

inputs = [f for f in listdir(input_path) if isfile(join(input_path, f)) and ".naf" in f]
for f in inputs:
    output_filename = f.split(".naf")[0] + ".txt"
    content = open(input_path + "/" + f, 'r').read()
    if ".bz2" in f:
        content = bz2.decompress(content)
    output_file = open(output_path + output_filename, 'w')
    output_file.write(extract_raw(content))
    output_file.close()
