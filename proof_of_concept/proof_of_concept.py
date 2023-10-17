# Proof_of_concept.py
# Mon 10/16/23 13:57:24
# By Azuhmier

import sys
import json
import os
import copy
import pprint
path = ("/Users/Azuhmier/progs/ohmfa/proof_of_concept/testbin.txt")
file = open(path, 'r')
Lines = file.readlines()

dspt = [ { "pattern":"by ",  "type":"author", "hiearchy":1, "keep_pattern":0, "end_pattern":"`"},
         { "pattern":">",    "type":"title",  "hiearchy":2, "keep_pattern":0, "end_pattern":"`"},
         { "pattern":"http", "type":"url",    "hiearchy":3, "keep_pattern":1, "end_pattern":"`"} ]

node_template = {"type":None, "value":None, "parent":None, "childs":[], "hiearchy":None}
tree = copy.deepcopy(node_template)
tree["type"] = "root"
tree["value"] = "ROOT"
tree["hiearchy"] = 0
node = tree
for line in Lines :
    match = None
    for thing in dspt :
       pattern = thing["pattern"]
       result = line.find(pattern)
       if result == 0 :
           start = result + len(pattern)
           if thing["keep_pattern"] == 0 :
               match = line[start:]
           else :
               match = line[0:]

           if thing["end_pattern"] is not None :
               end = match.find(thing["end_pattern"])
               if end != -1 :
                   match = match[:end]

           parent = None
           while parent == None :
               node_hiearchy  = node["hiearchy"]
               thing_hiearchy = thing["hiearchy"]
               if node["type"] == "root" :
                   parent = node
                   break
               elif node_hiearchy < thing_hiearchy :
                   parent = node
                   break
               else :
                   node     = node["parent"]
           node             = copy.deepcopy(node_template)
           node["type"]     = thing["type"]
           node["value"]    = match.strip()
           node["hiearchy"] = thing["hiearchy"]
           node["pattern"] = thing["pattern"]
           node["parent"]   = copy.copy(parent)
           parent["childs"].append(copy.copy(node))


def recurse(node, lvl) :
    print("    "*lvl + str(node["value"]))
    lvl = lvl + 1
    for child in node["childs"] :
       recurse(child,lvl)
lvl = 0
#recurse(tree, lvl)

def writeit(node) :
    if node["type"] != "root" :
        if node["type"] == "author" :
            print("")
            print("-"*80)
            print("-"*80)
        #elif node["type"] != "url" :
        elif node["type"] == "title" :
            print("")
        print( str(node["pattern"]) + str(node["value"]) )
    for child in node["childs"] :
       writeit(child)

writeit(tree)


