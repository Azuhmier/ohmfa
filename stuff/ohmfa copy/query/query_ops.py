#!/usr/bin/env python3
import pprint
import os
import re
import sys
import json


class QueryOps():


### Globals

rel_path_to_lib_parse_dir = '../../db/parse'
file_name_ops_json = 'ops.json'
file_name_ops_types_json = 'ops_types.json'
rel_path_To_lib_analysis_dir = '../../db/analysis'
file_name_ops_value = 'ops_values.json'
file_name_ops_void = 'ops_void.json'
rel_path_to_lib_resolve_dir = '../../db/resolve'
table_uid_ops = {}
table_types_uid_ops = {}
table_types_value_ops = {}
table_types_void_ops = {}

def insert_str(idx, substring, string) :
    new_string = string[:idx] + substring + string[idx:]
    return new_string

def insert_mult_str(args, string) :
    list_chars = list(string)
    for i, arg in enumerate(args) :
        idx = arg[0]+i
        substring = arg[1]
        list_chars.insert(idx, substring)
    return ''.join(list_chars)

def get_node(uid):
    node = table_uid_ops[uid]
    return node

def get_childs(uid):
    node = get_node(uid)
    child_uids = node['child_uids']
    return child_uids

def get_parent(uid):
    node = get_node(uid)
    puid = node['parent_uid']
    return puid


### Methods

def __init():
    """_summary_

    Returns:
        _type_: _description_
    """
    dir_parse_ops = get_abs_path_from_rel_path(rel_path_to_lib_parse_dir)
    file_path_ops_json = os.path.join(dir_parse_ops,file_name_ops_json)
    file_path_ops_types_json = os.path.join(dir_parse_ops,file_name_ops_types_json)
    table_uid_ops  = import_from_json(file_path_ops_json)
    table_types_uid_ops = import_from_json(file_path_ops_types_json)
    dir_analysis_ops = get_abs_path_from_rel_path(rel_path_To_Lib_Analysis_Dir)
    file_path_ops_value = os.path.join(dir_analysis_ops,file_name_ops_value)
    file_path_ops_void = os.path.join(dir_analysis_ops,file_name_ops_void)
    table_types_value_ops  = import_from_json(file_path_ops_value)
    table_types_void_ops = import_from_json(file_path_ops_value)
    return table_uid_ops, table_types_uid_ops, table_types_value_ops, table_types_void_ops

def summarize_value_table(value_table, value_type=None) :
    types = None
    if value_type is not None :
        types = [value_type]
    else :
        types = list(value_table.keys())
    for type in types :
        print(type)
        values = list(value_table[type].keys())
        values.sort()
        for value in values:
            cnt = str(len(value_table[type][value]['nodes'])) + ")"
            print(f"    ({cnt:<5}{value}")

def print_node_2(uid,lvl=0) :
    node = get_node(uid)
    tab = "----"*lvl
    if node['type'] == 'root' :
        print(node['type']+" "+tab+'root')
    elif node['type'] == 'VOID' :
        print(node['type']+"   "+tab+node['data_line'])
    elif node['type'] == 'thread':
        print(node['type']+" "+tab+node['value'])
    elif node['type'] == 'author':
        print(node['type']+" "+tab+node['value'])
    elif node['type'] == 'edition':
        print(node['type']+""+tab+node['value'])
    elif node['type'] == 'header':
        print(node['type']+" "+tab+node['value'])
    elif node['type'] == 'title':
        print(node['type']+"  "+tab+node['value'])
    elif node['type'] == 'url':
        print(node['type']+"    "+tab+node['value'])
    childs = get_childs(uid)
    for child in childs :
        print_node_2(child,lvl+1)

def print_node(uid,lvl=0) :
    node = get_node(uid)
    args = None
    if node['type'] == 'root' :
        print('%%%%%%%% ROOT %%%%%%%%%%')
    elif node['type'] == 'VOID' :
        print(node['data_line'])
    elif node['type'] == 'thread':
        print("-------##"+node['value'])
    elif node['type'] == 'author':
        if node['span2'][0] == -1:
            args = [[0,'<A>'],
                    [0,'<d>{'],
                    [node['span'][0],'}</d>'],
                    [node['span'][0],'<v>{'],
                    [node['span'][1],'}</v>'],
                    [len(node['data_line']),'</A>'], ]
        else :
            args = [[0,'<A>'],
                    [0,'<d>{'],
                    [node['span'][0],'}</d>'],
                    [node['span'][0],'<v>{'],
                    [node['span'][1],'}</v>'],
                    [node['span2'][0],'<a>{'],
                    [node['span2'][1],'}</a>'],
                    [len(node['data_line']),'</A>'], ]
    elif node['type'] == 'edition':
        args = [[0,'<E>'],
                [0,'<d>{'],
                [node['span'][0],'}</d>'],
                [node['span'][0],'<v>{'],
                [node['span'][1],'}</v>'],
                [len(node['data_line']),'</E>'], ]
    elif node['type'] == 'header':
        args = [[0,'<H>'],
                [node['span2'][0],'<a>{'],
                [node['span2'][1],'}</a>'],
                [node['span'][0],'<v>{'],
                [node['span'][1],'}</v>'],
                [len(node['data_line']),'</H>'], ]
    elif node['type'] == 'title':
        if node['span2'][0] == -1:
            args = [[0,'<T>'],
                    [0,'<d>{'],
                    [node['span'][0],'}</d>'],
                    [node['span'][0],'<v>{'],
                    [node['span'][1],'}</v>'],
                    [len(node['data_line']),'</T>'], ]
        else :
            args = [[0,'<T>'],
                    [0,'<d>{'],
                    [node['span'][0],'}</d>'],
                    [node['span'][0],'<v>{'],
                    [node['span'][1],'}</v>'],
                    [node['span2'][0],'<a>{'],
                    [node['span2'][1],'}</a>'],
                    [len(node['data_line']),'</T>'], ]
    elif node['type'] == 'url':
        if node['span2'][0] == -1:
            args = [[0,'<U>'],
                    [0,'<d>{'],
                    [node['span'][0],'}</d>'],
                    [node['span'][0],'<v>{'],
                    [node['span'][1],'}</v>'],
                    [len(node['data_line']),'</U>'], ]
        else :
            args = [[0,'<U>'],
                    [0,'<d>{'],
                    [node['span'][0],'}</d>'],
                    [node['span'][0],'<v>{'],
                    [node['span'][1],'}</v>'],
                    [node['span2'][0],'<a>{'],
                    [node['span2'][1],'}</a>'],
                    [len(node['data_line']),'</U>'], ]
    if args is not None :
        line = insert_mult_str(args, node['data_line'])
        print(line)
    childs = get_childs(uid)
    for child in childs :
        print_node(child,lvl+1)

table_uid_ops, table_types_uid_ops, table_types_value_ops, table_types_void_ops = __init()
print_node('P0L0')
print_node_2('P0L0')
summarize_value_table(table_types_value_ops)
