#! /usr/bin/env python

import argparse
from attr import attributes
import yaml
import pprint

def load_mdf_file(mdf_file_name):
    #Take a file text name, convert the yaml to a python object and return the python object
    with open(mdf_file_name,'r') as file:
        yamlobject = yaml.safe_load(file)
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
    #Create the attributes dictionary
    attributedict = {'attributes': propertylist}
    #Get the class json object for the key 'classes'.  This should get all classes/nodes
    classjson = linkmljson['classes']
    #Assign the attribute dictionary to the class json with the node as the key.  Currently doesn't check if the key has been assigned before
    classjson[nodename] = attributedict
    #Tack on description, is_a, required
    classjson[nodename]['description'] = description
    classjson[nodename]['is_a'] = isathing
    linkmljson['classes'] = classjson
    return linkmljson

def updateFieldname(name):
    corrections = {'Desc':'description', 'Req':'required'}
    if name in corrections:
        name = corrections[name]
    return name

def updateValues(name):
    corrections = {'Yes': 'true', 'No' :'false', 'Preferred': 'true'}
    if name in corrections:
        name = corrections[name]
    return name

def propertyLookup(propertydict, propertylist, fieldlist):
    #Create the list that evenetually gets returned
    updateddictionary = []
    #For each attribute in the property list, see if the attribute is in the dictionary
    if propertylist is not None:
        for property in propertylist:
            newvalue = None
            if property in propertydict:
                tempdict = {}
                for field in fieldlist:  #Desc, Req
                    if field in propertydict[property]:
                        newvalue = propertydict[property][field]
                        newvalue = updateValues(newvalue)
                        field = updateFieldname(field)
                        tempdict[field] =newvalue
                if tempdict:  #tempdict is NOT empty
                    finaltemp = {}
                    finaltemp[property] = tempdict
                    updateddictionary.append(finaltemp)
                else:
                    updateddictionary.append(property)
            else:
                updateddictionary.append(property)
    return updateddictionary







def main(args):
    modelobject = load_mdf_file(args.modelfile)
    propsobject = load_mdf_file(args.propsfile)
    nodedictionary = modelobject['Nodes']
    propertydict = propsobject['PropDefinitions']
    linkmljson = {}
    linkmljson['classes'] = {}

    for nodename in nodedictionary.keys():
        isathing = nodedictionary[nodename]['Tags']['Category']
        nodeDescription = nodedictionary[nodename]['Desc']
        propertylist = nodedictionary[nodename]['Props']
        #Need to provide a dictionary of MDF attribues to look for and their LinkML counterparts
        fieldlist = {'Req' : 'request', 'Desc' : 'description'}
        propertylist = propertyLookup(propertydict, propertylist,fieldlist)
        linkmljson = buildLinkml(linkmljson, nodename, nodeDescription, isathing, propertylist)

    write_linkml_file(linkmljson, args.outputfile)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--modelfile", required = True, help="MDF model file")
    parser.add_argument("-p", "--propsfile", required = True, help = "MDF Properties file")
    parser.add_argument("-o", "--outputfile", required = True, help = "LinkML YAML file")

    args = parser.parse_args()
    main(args)