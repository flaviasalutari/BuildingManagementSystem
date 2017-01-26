import sys


config_dicts = {
"perc_tints" : {1 : 0.58, 2: 0.40, 3 : 0.10, 4: 0.01},
"classA" : 100, # get from a configuration file
"q_iaq" : 47,
"f_occupation" : 8/24, # get from a configuration file
"volume" : 4.44 * 5 * 5 # get from a configuration file 
}

try:
    obj = config_dicts
    perc_tints = obj["perc_tints"]
    classA = obj["classA"]
    q_iaq = obj["q_iaq"]
    f_occupation = obj["f_occupation"]
    volume = obj["volume"]
except:
    sys.exit("Error in opening the file for retrieving the info from config_dicts")



