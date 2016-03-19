import sys
import os
import urllib2
import requests
import pdb
import time
import math
import time


ner_command = "java -mx700m -cp ./stanford-ner.jar:./lib/* edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier ./classifiers/english.all.3class.distsim.crf.ser.gz"
api_key = os.environ.get('BING_API_KEY')
space = '%20'
doublequote = '%22'
singlequote = '%27'

def extract_named_entities(path):
    entities = {}
    ner_input_file = open('ner_input.txt', 'w')
    for filename in os.listdir(path):
        with open(path+filename, 'r') as f:
            entities[filename] = []
            ner_input_file.write('------------SATIRE-SEPARATOR<<<' + filename + '>>>------------\n')
            ner_input_file.write(f.read())
    ner_input_file.close()
    os.system(ner_command + ' -textFile ner_input.txt -outputFormat inlineXML > ner_output.txt')
    file = open('ner_output.txt', 'r')
    for line in file.readlines():
        if '------------SATIRE-SEPARATOR' in line:
           current_filename = line.split("SATIRE-SEPARATOR<<<")[1].split(">>>")[0] 
        orgs = line.split("<ORGANIZATION>")[1:]
        for org in orgs:
            org_name = org.split("</ORGANIZATION>")[0].rstrip()
            entities[current_filename] += [org_name] 

        people = line.split("<PERSON>")[1:]
        for person in people:
            person_name = person.split("</PERSON>")[0].rstrip()
            entities[current_filename] += [person_name] 
    os.system("rm ner_input.txt ner_output.txt")
    return entities

def extract_bing_results(query):
    try:
        query_term = singlequote 
        for item in query:
            query_term += doublequote + item.replace(' ',space) + doublequote + space 
        query_term += singlequote
        url = 'https://api.datamarket.azure.com/Data.ashx/Bing/Search/Composite?Sources=%27web%27&Query=' + query_term + '&$format=Json'
        r = requests.get(url, auth=("", api_key))
        return int(r.json()[u'd'][u'results'][0]['WebTotal']) + 1
    except:
        return 1

def compute_validity(path):
    output_file = open('semantic_validity.txt', 'w')
    feature = {}
    entity_db = extract_named_entities(path)
    for filename in entity_db.keys():
        feature[filename] = extract_bing_results(set(entity_db[filename]))
        print filename + ": " + str(feature[filename]) + str(entity_db[filename])
        output_file.write(filename + '\t' + str(math.log(feature[filename])) + '\n')

