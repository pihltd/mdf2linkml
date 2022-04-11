import yaml

def load_mdf_file(mdf_file_name):
    #Take a file text name, convert the yaml to a python object and return the python object
    with open(mdf_file_name,'r') as file:
        yamlobject = yaml.safe_load(file)
    return yamlobject