#!/usr/bin/env python3
import pprint
import os
import re
import sys
import json


class AnalyzeOps():


### Globals
opts = {"updateOnly":True,"verbose":True}
if not opts['verbose'] :
    sys.stdout = open(os.devnull, 'w')
rel_path_to_lib_parse_dir = '../../db/parse'
file_name_ops_json = 'ops.json'
filename_ops_types_json = 'opsTypes.json'
rel_path_to_lib_analysis_dir = '../../db/analysis'
filename_ops_value = 'opsValues.json'
filename_ops_void = 'opsVoid.json'
rel_path_to_lib_resolve_dir = '../../db/Resolve'
table_uid_ops = {}
table_types_uid_ops = {}
table_types_value_ops = {}
table_types_void_ops = {}
# Utilities

def get_parent(node):
    """_summary_

    Args:
        node (_type_): _description_

    Returns:
        _type_: _description_
    """
    puid = node['parentUID']
    parent = table_uid_ops[puid]
    return parent

def get_childs(node):
    """_summary_

    Args:
        node (_type_): _description_

    Returns:
        _type_: _description_
    """
    child_uids = node['child_uids']
    childs = []
    for cuid in child_uids :
        childs.append(table_uid_ops[cuid])
    return childs

def get_node(uid):
    """_summary_

    Args:
        uid (_type_): _description_

    Returns:
        _type_: _description_
    """
    node = table_uid_ops[uid]
    return node

def get_abs_path_from_rel_path(rel_path_arg):
    """_summary_

    Args:
        rel_path_arg (_type_): _description_

    Returns:
        _type_: _description_
    """
    dir_cur_script = os.path.dirname(__file__)
    dirty_abs_path_arg = os.path.join(dir_cur_script, rel_path_arg)
    abs_path_arg = os.path.abspath(dirty_abs_path_arg)
    return abs_path_arg

def import_from_json(path):
    """_summary_

    Args:
        path (_type_): _description_

    Returns:
        _type_: _description_
    """
    with open(path, "r") as openfile:
        dict = json.load(openfile)
    return dict

def export_to_json(filePath,dict) :
    """_summary_

    Args:
        filePath (_type_): _description_
        dict (_type_): _description_
    """
    json_object = json.dumps(dict, indent=4)
    with open(filePath, "w+") as outfile :
        outfile.write(json_object)

def __export_value_table() :
    """_summary_
    """
    dir_lib_analysis = get_abs_path_from_rel_path(rel_path_to_lib_analysis_dir)
    file_path_ops_value_json = os.path.join(dir_lib_analysis,filename_ops_value)
    file_path_ops_void_json = os.path.join(dir_lib_analysis,filename_ops_void)
    export_to_json(file_path_ops_value_json,table_types_value_ops)
    export_to_json(file_path_ops_void_json,table_types_void_ops)

### Methods

def __gen_value_table (type_table) :
    """_summary_

    Args:
        type_table (_type_): _description_

    Returns:
        _type_: _description_
    """
    value_table = {}
    void_table = {}
    for type in type_table :
        value_table[type] = {}
        for uid in type_table[type] :
            node = get_node(uid)
            if node['value'] is not None :
                if node['value'].lower() not in value_table[type] :
                    value_table[type][node['value'].lower()] = {}
                    value_table[type][node['value'].lower()]['nodes'] = []
                value_table[type][node['value'].lower()]['nodes'].append(uid)
                value_table[type][node['value'].lower()]['type'] = 'value'
            elif node['data_line'] is not None:
                if node['data_line'].lower() not in value_table[type] :
                    value_table[type][node['data_line'].lower()] = {}
                    value_table[type][node['data_line'].lower()]['nodes'] = []
                value_table[type][node['data_line'].lower()]['nodes'].append(uid)
                value_table[type][node['data_line'].lower()]['type'] = 'data_line'
            else :
                if type not in void_table :
                    void_table[type]=[]
                void_table[type].append(uid)
    return value_table, void_table

def __init():
    """_summary_

    Returns:
        _type_: _description_
    """
    dir_parse_ops = get_abs_path_from_rel_path(relPathToLib_Parse_Dir)
    file_path_ops_json = os.path.join(dir_parse_ops,file_name_ops_json)
    file_path_ops_types_json = os.path.join(dir_parse_ops,filename_ops_types_json)
    table_uid_ops  = import_from_json(file_path_ops_json)
    table_types_uid_ops = import_from_json(file_path_ops_types_json)
    return table_uid_ops, table_types_uid_ops
table_uid_ops, table_types_uid_ops =  __init()
table_types_value_ops, table_types_void_ops = __gen_value_table(table_types_uid_ops)

__export_value_table()
