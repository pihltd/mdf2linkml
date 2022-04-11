#! /usr/bin/env python

import argparse
from ctypes.wintypes import PPOINT
import yaml
import pprint

def load_mdf_file(mdf_file_name):
    #Take a file text name, convert the yaml to a python object and return the python object
    with open(mdf_file_name,'r') as file:
        yamlobject = yaml.safe_load(file)
    return yamlobject

def parse_model_nodes(yamlobject):
    #Parses out all of the MDF nodes
    mdfkeys = ['Desc', 'Props']
    #Ignore the mdf Tags, those are used by Bento to control site behavior, they're not part of the model
    nodearray = yamlobject['Nodes']
    for mdfnode in nodearray:
        pprint.pprint(mdfnode)
        for mdfkey in mdfkeys:
            pprint.pprint(nodearray[mdfnode][mdfkey])
        #pprint.pprint(nodearray[mdfnode])

def main(args):
    modelobject = load_mdf_file(args.modelfile)
    propsobject = load_mdf_file(args.propsfile)
    modeldict = modelobject['Nodes']
    propsdict = propsobject['PropDefinitions']
    for key in modeldict.keys():
        for property in modeldict[key]['Props']:
            print(key)
            print(property)
            pprint.pprint(propsdict[property]['Desc'])
    #print(type(modelkeys))
    #pprint.pprint(yamlobject)
    #parse_model_nodes(modelobject)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--modelfile", required = True, help="MDF model file")
    parser.add_argument("-p", "--propsfile", required = True, help = "Output file")

    args = parser.parse_args()
    main(args)