#! /usr/bin/env python

import argparse
import yaml
import pprint

def load_mdf_file(mdf_file_name):
    #Take a file text name, convert the yaml to a python object and return the python object
    with open(mdf_file_name,'r') as file:
        yamlobject = yaml.safe_load(file)
        #yamlobject = yaml.load(file)
    return yamlobject

def write_linkml_file(modeljson, filename):
    outfile = open(filename,'w')
    yaml.safe_dump(modeljson, outfile)
    outfile.close()


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

def parse_classes(nodeobject):
    #MDF (well, ICDC at least), uses Tags -> Categories to organize data elements.  Those are likely candidates for LinkmlClasses
    classlist = []
    for node in nodeobject.keys():
        classlist.append(nodeobject[node]['Tags']['Category'])
    return classlist

def buildLinkml(linkmljson, nodename, description, isathing, propertylist):
    """LinkML JSON structure
    {'classes': {classname: {attributes:[attributenames]}}}
    """
    #Step one, create the attributes list
    attributedict = {'attributes': propertylist}
    classjson = linkmljson['classes']
    classjson[nodename] = attributedict
    classjson[nodename]['description'] = description
    classjson[nodename]['is_a'] = isathing
    linkmljson['classes'] = classjson
    return linkmljson



def main(args):
    modelobject = load_mdf_file(args.modelfile)
    #propsobject = load_mdf_file(args.propsfile)
    modelnodedict = modelobject['Nodes']
    #propertyobject = propsobject['PropDefinitions']
    linkmljson = {}
    linkmljson['classes'] = {}
    for nodename in modelnodedict.keys():
        isathing = modelnodedict[nodename]['Tags']['Category']
        description = modelnodedict[nodename]['Desc']
        propertylist = modelnodedict[nodename]['Props']
        linkmljson = buildLinkml(linkmljson, nodename, description, isathing, propertylist)
    #pprint.pprint(linkmljson)
    write_linkml_file(linkmljson, args.outputfile)



    #for key in modeldict.keys():
    #    for property in modeldict[key]['Props']:
    #        print(key)
    #        print(property)
    #        pprint.pprint(propsdict[property]['Desc'])
    #print(type(modelkeys))
    #pprint.pprint(yamlobject)
    #parse_model_nodes(modelobject)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--modelfile", required = True, help="MDF model file")
    parser.add_argument("-p", "--propsfile", required = True, help = "MDF Properties file")
    parser.add_argument("-o", "--outputfile", required = True, help = "LinkML YAML file")

    args = parser.parse_args()
    main(args)