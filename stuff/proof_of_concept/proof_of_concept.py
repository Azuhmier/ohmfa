# Proof_of_concept.py
# Mon 10/16/23 13:57:24
# By Azuhmier

#import sys
#import json
#import os
import copy
#import pprint
path = ("./proof_of_concept/testbin.txt")
file = open(path, 'r')
Lines = file.readlines()

class Pattern:
    pattern: str
    pat_type: str
    hierarchy: int
    keep_pat: bool
    end_pat: str

    def __init__(self, pattern: str, pat_type: str, hierarchy: int, keep_pat: bool, end_pattern: str):
        self.pattern = pattern
        self.pat_type = pat_type
        self.hierarchy = hierarchy
        self.keep_pat = keep_pat
        self.end_pat = end_pattern

patterns: list[Pattern] = [Pattern("by ", "author", 1, False, "`"), Pattern(">", "title", 2, False, "`"), Pattern("http", "url", 3, True, "`")]

# this `Pattern` class, and the list of patterns, should be a good replacement
# for the pattern dictionary that's below.

dspt = [ { "pattern":"by ",  "type":"author", "hierarchy":1, "keep_pattern":0, "end_pattern":"`"},
         { "pattern":">",    "type":"title",  "hierarchy":2, "keep_pattern":0, "end_pattern":"`"},
         { "pattern":"http", "type":"url",    "hierarchy":3, "keep_pattern":1, "end_pattern":"`"} ]


node_template = {"type": None, "value": None, "parent": None, "children": [], "hierarchy": None}
tree = copy.deepcopy(node_template)
tree["type"] = "root"
tree["value"] = "ROOT"
tree["hierarchy"] = 0

node = tree
for line in Lines:
    match = None
    for thing in dspt:
       pattern = thing["pattern"]
       result = line.find(pattern)
       if result == 0:
           start = result + len(pattern)
           if thing["keep_pattern"] == 0:
               match = line[start:]
           else:
               match = line

           if thing["end_pattern"] is not None:
               end = match.find(thing["end_pattern"])
               if end != -1:
                   match = match[:end]

           parent = None
           while parent is None:
               thing_hierarchy = thing["hierarchy"]
               node_hierarchy = node["hierarchy"]
               if node["type"] == "root" or node_hierarchy < thing_hierarchy:
                   parent = node
                   break
               else:
                   node     = node["parent"]
                   
           node             = copy.deepcopy(node_template)
           node["type"]     = thing["type"]
           node["value"]    = match.strip()
           node["hierarchy"] = thing["hierarchy"]
           node["pattern"] = thing["pattern"]
           node["parent"]   = copy.copy(parent)
           parent["children"].append(copy.copy(node))


def recurse(node, lvl=0):
    print("    "*lvl + str(node["value"]))
    lvl += 1
    for child in node["children"]:
       recurse(child,lvl)
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
        print(f'{node["pattern"]}{node["value"]}') 
    for child in node["children"] :
       writeit(child)

writeit(tree)


