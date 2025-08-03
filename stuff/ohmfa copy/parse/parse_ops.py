#!/usr/bin/env python3
import os
import re
import sys
import json


class ParseOps(): 


opts = {"updateOnly":True,"verbose":True}
if not opts['verbose'] :
    sys.stdout = open(os.devnull, 'w')

### Globals ###
ov={
    'tree': {},
    'node_table':{},
    'uid_table':{},
    'uid_type_table':{},
    'node_ord': { 
        'root':0,
        'thread':1,
        'header':2,
        'edition':2,
        'author':2,
        'title':3,
        'url':4 }, }
node_ord   = ov['node_ord']
node_table = ov['node_table']
uid_table = ov['uid_table']
uid_type_table = ov['uid_type_table']

### utilities ###

def __add_to_node_table(node) :
    if node['type'] not in node_table.keys() :
        node_table[node['type']]=[]
    node_table[node['type']].append(node)

def __gen_node(type=None) :
    node = {'UID':None,
            'type':type,
            'data_line':None,
            'value':None,
            'span':None,
            'span2':None,
            'parent':None,
            'childs':[], }
    return node

def __get_valid_parent(node, parent_node=None) :
    if node['type'] != 'VOID' :
        if node['type'] != 'root' :
            while node_ord[node['type']] <= node_ord[parent_node['type']]:
                parent_node = parent_node['parent']
    return parent_node


### methods ###
def __link_node(node, parent_node=None):
    parent_node = __get_valid_parent(node,parent_node)
    __add_to_node_table(node)
    if node['type'] != 'root' :
        if node['type'] != 'VOID' or parent_node['type'] == 'root' :
            parent_node['childs'].append(node)
            node['parent'] = parent_node
        else :
            parent_node['parent']['childs'].append(node)
            node['parent'] = parent_node['parent']
    if node['type'] != 'VOID' :
        parent_node = node
    return parent_node

def __init():
    node = __gen_node('root')
    ov['tree'] = node
    node = ov['tree']
    node['UID']="P0L0"
    parent_node = __link_node(node)
    node = None
    return node, parent_node

def __parse_data_from_op_text():
    rel_path_to_ops_db_dir = '../../db/parse'
    dir_ops_db = get_abspath_from_rel_path(rel_path_to_ops_db_dir)
    rel_path_to_ops_dir = '../../threads/ops'
    dir_ops_texts = get_abspath_from_rel_path(rel_path_to_ops_dir)
    thread_num_list = list_dir_no_hidden(dir_ops_texts)
    re_title = re.compile("^>([^\[(]+?)<*(?:(?:\s*-*\s*[\[(]\s*([^\[\]()]+)\s*[\])])|(?:\s+-\s+(.+)|\s+((?:pt\.?|part|ch\.?|chapter)\s+\d+)|))$")
    re_author = re.compile("^[bB]y\s([^\[(]+?)(?:[- ]*[\[(]\s*([^\[\]()]+)\s*[\])])*$")
    re_url =  re.compile("^(http[^ ]+)(?:[- ]*[\[(]\s*([^\[\]()]+)\s*[\])])*$")
    re_edition = re.compile(r"^(?:>|\")\s*([^>\"]+)\s*(?:<|\")\s*\w*$")
    re_header = re.compile("^/(\w+)/.*#(\d+)$")
    node, parent_node = __init()
    for threadnum in thread_num_list :
        op_file_folder_path = os.path.join(dir_ops_texts,threadnum)
        op_file_path = os.path.join(op_file_folder_path,threadnum+".txt")
        with open(op_file_path,'r') as f:
            lines = f.readlines()
            node = __gen_node('thread')
            node['UID']="P"+threadnum+"L"+str(0)
            node['value']=threadnum
            parent_node = __link_node(node,parent_node)
            for cnt,line in enumerate(lines) :
                uid = "P"+threadnum+"L"+str(cnt+1)
                line = re.sub(r'\s+',' ',line)
                line = line.rstrip()
                line = line.lstrip()
                node=__gen_node()
                node['UID']=uid
                node['data_line']=line
                header  = re_header.match(line)
                edition  = re_edition.match(line)
                author = re_author.match(line)
                title = re_title.match(line)
                url  = re_url.match(line)
                if header :
                    value = line[header.span(1)[0]:header.span(1)[1]]
                    node['value']=value
                    node['type']='header'
                    node['span']=header.span(1)
                    node['span2']=header.span(2)
                elif edition :
                    value = line[edition.span(1)[0]:edition.span(1)[1]]
                    node['value']=value
                    node['type']='edition'
                    node['span']=edition.span(1)
                elif title :
                    value = line[title.span(1)[0]:title.span(1)[1]]
                    node['value']=value
                    node['type']='title'
                    node['span']=title.span(1)
                    node['span2']=title.span(2)
                elif author :
                    value = line[author.span(1)[0]:author.span(1)[1]]
                    node['value']=value
                    node['type']='author'
                    node['span']=author.span(1)
                    node['span2']=author.span(2)
                elif url :
                    value = line[url.span(1)[0]:url.span(1)[1]]
                    node['value']=value
                    node['type']='url'
                    node['span']=url.span(1)
                    node['span2']=url.span(2)
                else :
                    node['type']='VOID'
                parent_node = __link_node(node,parent_node)
    __gen_uid_table(ov['tree'])
    __gen_uid_type_table()
    json_object = json.dumps(ov["uid_table"], indent=4)
    file_path_ops_db = os.path.join(dir_ops_db,"ops.json")
    with open(file_path_ops_db, "w") as outfile:
        outfile.write(json_object)
    json_object = json.dumps(ov["uid_type_table"], indent=4)
    file_path_ops_types_db = os.path.join(dir_ops_db,"opsTypes.json")
    with open(file_path_ops_types_db, "w") as outfile:
        outfile.write(json_object)

def __gen_uid_type_table() :
    for type in node_table :
        ov['uid_type_table'][type]=[]
        for node in node_table[type]:
            ov['uid_type_table'][type].append(node['UID'])

def __gen_uid_table(node) :
    puid = None
    cuid = []
    if node['type'] != 'root' :
        puid = node['parent']['UID']
    keys = set(node) - set(['parent','childs'])
    copied_node = { k:node[k] for k in keys}
    copied_node['parentUID'] = puid
    copied_node['childUIDs'] = cuid
    uid_table[copied_node['UID']] = copied_node
    for child in node['childs'] :
        uid_table[copied_node['UID']]['childUIDs'].append(child['UID'])
        __gen_uid_table(child)

__parse_data_from_op_text()
