#!/usr/bin/env python3
import pprint
import os
import re
import sys
import json


class ResolveOps():
### Globals

ov = {
    'h': {},
    'b': {},
    'p': {
        'top':
            '../..',
            'bt_values':'db/buffers/t_values',
            'bvalues':'db/buffers/values.txt',
            'ht_uids':'db/parse/opsTypes.json',
            'huidStats':'db/analysis/uid_stats.json',
            'ht_values':'db/analysis/ops_values.json',
            'huids':'db/parse/ops.json',
            'ht_value_stats':'db/analysis/uid_stats.json',
            'ht_value_aliases':'db/resolve/t_value_aliases.json'},
        'c': {
            't_lvls' : {
                'root':0,
                'thread':1,
                'header':2,
                'edition':2,
                'author':2,
                'title':3,
                'url':4,
                'VOID':4, },
            'h_import': [
                'uids',
                't_uids',
                't_values'],
            'b_import': [
                't_values',
                'values', ],
            'h_export': [
                'uid_stats',
                't_value_stats',
                't_value_aliases'],
            'b_export': [
                't_values',
                'values'],
            't_valid_ptypes' : {
                'root':['root'],
                'thread':['root'],
                'header':['thread'],
                'edition':['thread'],
                'author':['thread'],
                'title':['author'],
                'url':['title'],
                'VOID':[],} } }

# Utilities

def get_node(uid):
    node = ov['h']['uids'][uid]
    return node

def get_p_uid(uid):
    node = get_node(uid)
    p_uid = node['parentUID']
    return p_uid

def get_c_uids(uid):
    node = get_node(uid)
    cuids = node['childUIDs']
    return cuids

def get_from_node(uid,key):
    node = get_node(uid)
    res = node[key]
    return res

def get_lvl(uid):
    type = get_from_node(uid,'type')
    lvl = ov['c']['t_lvls'][type]
    return lvl

def valid_p_lvl(uid,p_uid):
    res = False
    lvl = get_lvl(uid)
    plvl = get_lvl(p_uid)
    if (lvl - plvl) == 1 :
        res = True
    return res

def valid_p_type(uid,p_uid):
    res = False
    type = get_from_node(uid,'type')
    p_type = get_from_node(p_uid,'type')
    valid_p_types = ov['c']['t_valid_ptypes'][type]
    if p_type in valid_p_types:
        res = True
    return res

def get_value_node(value, type)  :
    value_node = ov['h']['t_values'][type][value]
    return value_node

def get_value(uid):
    node = get_node(uid)
    type = node['type']
    value = None
    if node['value'] is not None:
        value = node['value']
    elif node['data_line'] is not None:
        value = node['data_line']
    return value,type

### Hash Methods

def gen_h_t_value_aliases():
    """
    h_name = 't_value_aliases'
    u_name = 'h'+h_name
    rel_path = ov['p'][u_name]
    abs_path = get_abs_path(rel_path)
    ov['h']['t_value_aliases']={}
    for type in ov['h']['t_values'] :
        ov['h']['t_value_aliases'][type]={}

def gen_h_uid_stats():
    h_name = 'uid_stats'
    u_name = 'h' + h_name
    uid_stats={}
    for uid in ov['h']['uids']:
        uid_stats[uid]={'pdiff' : False, 'p_type': False}
        p_uid = get_p_uid(uid)
        if p_uid is not None :
            if valid_p_lvl(uid,p_uid) :
                uid_stats[uid]['pdiff'] = True
            if valid_p_type(uid,p_uid) :
                uid_stats[uid]['p_type'] = True
    ov['h'][h_name] = uid_stats

def gen_h_t_value_stats():
    t_value_stats={}
    t_values = ov['h']['t_values']
    uid_stats=ov['h']['uid_stats']
    for type in t_values   :
        t_value_stats[type]={}
        for value in t_values[type] :
            t_value_stats[type][value]={'p_value': False, 'parents': {}, }
            for uid in t_values[type][value]['nodes'] :
                p_uid=get_p_uid(uid)
                p_value, p_type = get_value(p_uid)
                if p_type not in t_value_stats[type][value]['parents'].keys():
                    t_value_stats[type][value]['parents'][p_type]={}
                if p_value not in t_value_stats[type][value]['parents'][p_type].keys():
                    t_value_stats[type][value]['parents'][p_type][p_value]={
                        'nodes':[]
                    }
                t_value_stats[type][value]['parents'][p_type][p_value]['nodes'].append(uid)
            keys = t_value_stats[type][value]['parents'].keys()
            if len(keys) == 1:
                values = t_value_stats[type][value]['parents'][list(keys)[0]].keys()
                if len(values) == 1 :
                    t_value_stats[type][value]['p_value'] = True
    ov['h']['t_value_stats']=t_value_stats

### Buffer Methods

def parse_b_t_values():
    b_name = 't_values'
    u_name = 'b'+b_name
    rel_path = ov['p'][u_name]
    abs_path = get_abs_path(rel_path)
    ov['b'][b_name] = {}
    for type in ov['h']['t_values']:
        ov['b'][b_name][type] = []
        file_path = os.path.join(abs_path,type+'.txt')
        if os.path.exists(file_path) :
            b = read_file(file_path)
            ov['b'][b_name][type] = b

def parse_b_values():
    b_name = 'values'
    u_name = 'b'+b_name
    rel_path = ov['p'][u_name]
    abs_path = get_abs_path(rel_path)
    ov['b'][b_name] = []
    if os.path.exists(abs_path) :
        b = read_file(abs_path)
        ov['b'][b_name] = b

def apply_b_t_values():
    b_name = 't_values'
    u_name = 'b'+b_name
    for type in ov['b'][b_name] :
        for line in ov['b'][b_name][type] :
            1;

def apply_b_values():
    """_summary_
    """
    b_name = 'values'
    u_name = 'b'+b_name
    for line in ov['b'][b_name] :
        1;

def gen_b_t_values():
    b_name = 't_values'
    u_name = 'b'+b_name
    for type in ov['h'][b_name] :
        lines = []
        values = list(ov['h']['t_values'][type].keys())
        values.sort()
        for value in values:
            lines.append(value)
        ov['b'][b_name][type] = lines

def gen_b_values():
    b_name = 'values'
    u_name = 'b'+b_name
    for type in ov['h']['t_values'] :
        line_parts = []
        values = list(ov['h']['t_values'][type].keys())
        for value in values:
            line_parts.append([value,type])
        sorted_line_parts= sorted(line_parts, key=lambda x: x[0])
        lines = []
        for part in sorted_line_parts:
            line = (part[0] +" | "+ part[1])
            lines.append(line)
        ov['b'][b_name] = lines

def write_b_t_values():
    b_name = 't_values'
    u_name = 'b'+b_name
    rel_path = ov['p'][u_name]
    abs_path = get_abs_path(rel_path)
    for type in ov['b'][b_name] :
        lines = ov['b'][b_name][type]
        text = '\n'.join(lines)
        filepath = os.path.join(abs_path,type+'.txt')
        write_file(filepath,text)

def write_b_values():
    b_name = 'values'
    u_name = 'b'+b_name
    rel_path = ov['p'][u_name]
    abs_path = get_abs_path(rel_path)
    lines = ov['b'][b_name]
    text = '\n'.join(lines)
    write_file(abs_path,text)

### Methods

def __init():
    for h_name in ov['c']['h_import'] :
        u_name = 'h'+h_name
        rel_path = ov['p'][u_name]
        abs_path = get_abs_path(rel_path)
        print("searching for "+abs_path)
        if os.path.exists(abs_path) :
            print(u_name +" found!")
            h = import_from_json(abs_path)
            ov['h'][h_name] = h
        else :
            print(u_name +" not found!")
            method_name = "gen"+u_name
            if method_name in list(globals().keys()) :
                print("generating "+u_name)
                globals()[method_name]()
    for b_name in ov['c']['b_import']:
        u_name = 'b'+b_name
        method_name = "parse"+u_name
        print("searching for method "+method_name)
        if method_name in list(globals().keys()) :
            print(method_name+" found!")
            globals()[method_name]()

def __gen_hashes() :
    for h_name in ov['c']['h_export'] :
        method_name = "genh"+h_name
        print("searching for method "+method_name)
        if method_name in list(globals().keys()) :
            print(method_name+" found!")
            globals()[method_name]()

def __apply_buffers() :
    for b_name in ov['c']['b_export'] :
        method_name = "applyb"+b_name
        if method_name in list(globals().keys()) :
            globals()[method_name]()

def __gen_buffers() :
    for b_name in ov['c']['b_export']:
        method_name = "genb"+b_name
        if method_name in list(globals().keys()) :
            globals()[method_name]()

def __export():
    for h_name in ov['c']['h_export']:
        u_name = 'h'+h_name
        rel_path = ov['p'][u_name]
        abs_path = get_abs_path(rel_path)
        export_to_json(abs_path,ov['h'][h_name])
    for b_name in ov['c']['b_export']:
        method_name = "writeb"+b_name
        if method_name in list(globals().keys()) :
            globals()[method_name]()

__init()
__gen_hashes()
__apply_buffers()
__gen_buffers()
__export()
#thread(#ofpost,time)
#value number
#child share table
