import os
import re
import json



class ImportRegex(): 




def import_from_json(file_path):
    """_summary_

    Args:
        file_path (_type_): _description_

    Returns:
        _type_: _description_
    """
    with open(file_path, "r") as open_file:
        json_dict = json.load(open_file)
    return json_dict

def get_abs_path(rel_path) :
    """_summary_

    Args:
        rel_path (_type_): _description_

    Returns:
        _type_: _description_
    """
    pwd = os.path.dirname(__file__)
    messy_abs_path = os.path.join(pwd, rel_path)
    abs_path = os.path.abspath(messy_abs_path)
    return abs_path

def read_file(file_path):
    """_summary_

    Args:
        file_path (_type_): _description_

    Returns:
        _type_: _description_
    """
    with open(file_path, "r", encoding="utf-8") as outfile :
        lines = outfile.read().splitlines()
    return lines

def __import_regexs():
    """_summary_

    Returns:
        _type_: _description_
    """
    file_path = get_abs_path('../../.ohmfa/hmofa/ops_regex.txt')
    lines = read_file(file_path)
    res = {}
    for line in lines :
        if line[0] != ' ' :
            node_type = line
            res[node_type]=[]
        else :
            line.rstrip()
            line=line.replace(' ','')
            res[node_type].append(line)
    for key in res :
        res[key] = ''.join(res[key])
    return res
regexes = __import_regexs()

def gen_lvls() :
    """_summary_
    """
        file_path = get_abs_path('../../.ohmfa/hmofa/ops_config.json')
        file_path2 = get_abs_path('../../.ohmfa/global/config.json')
        h = import_from_json(file_path)
        g = import_from_json(file_path2)
        lvls={}
        for type in g['types'] :
            lvls[type] = g['types'][type]['lvl']
        for type in h['types'] :
            rellvl = h['types'][type]['rel_lvl'][0]
            gtype = h['types'][type]['rel_lvl'][1]
            lvl = g['types'][gtype]['lvl']
            lvls[type] = rellvl+lvl
        print(lvls)
        diff = 1 - min(list(lvls.values()))
        for key in lvls :
            lvls[key] = lvls[key] + diff
        print(lvls)

gen_lvls()
