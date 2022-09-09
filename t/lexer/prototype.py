# lexer_test.py

import sys
import json
import os
#from os.path import dirname, abspath

#----------- IMPORT LEXER CLASS ------------ #
current      = os.path.dirname(os.path.realpath(__file__))
t_path       = os.path.dirname(current)
ohmfa_path   = os.path.dirname(t_path)
sys.path.append(ohmfa_path)

from lib.lexer import lexer


#----------- OPTIONS ------------ #
PrintTokenList     = False
LexerVerbose       = False
z_txt_test         = True
ze_line_test       = True
OutputTokesnAsJson = True
TOKENS_OUPUT_PATH  = "~/Desktop/tokens.json"
MFILE_PATH         = "../mfiles/hmofa.txt"
LEXER_CONFIG_PATH  = "../inputs/json/hmofa.json"


#----------- UTILITIES ------------ #
def import_txt(path) :
    path = os.path.expanduser(path)
    with open(path) as txt_file:
        return txt_file.read()
    return txt

def import_json(path) :
    path = os.path.expanduser(path)
    with open(path) as json_file:
        return json.load(json_file)

def write_json(data, path) :
    path = os.path.expanduser(path)
    with open(path, "w") as outfile:
        json.dump(data, outfile, indent=4, sort_keys=True)


#----------- LOAD FILES ------------ #
txt         = import_txt(MFILE_PATH)
LexerConfig = import_json(LEXER_CONFIG_PATH)


#----------- INITIATE LEXER AND GET TOKENS ------------ #
mylexer = lexer(txt, LexerConfig, LexerVerbose)
token   = {'controller_uid': 'A'}
tokens  = []

while token['controller_uid'] != '-1' :
    token = mylexer.get_token()
    tokens.append(token)


#----------- Print Token List ------------ #
if PrintTokenList :
    print("--------- TOKEN LIST ---------") # verbose
    for token in tokens : # verbose
        #print("j-14s %s" % (token['name'], token['match']))
        pos = "LN:%-4s (%-3s %-3s) z_txt:%-6s    " % (token['line_number'], token['z_line'],token['e_line'],token['z_data'])
        print("%-25s %-25s %-20s %s" % (pos, token['type'], token['controller_name'], token['match']))


#----------- Z_TXT TEST ------------ #
if z_txt_test :
    success = True
    print("...z_txt_test......",end='')
    for token in tokens : # verbose
        if token['match'] is not None :
            z_txt = token['z_data']
            e_txt =  token['z_data'] + token['e_line'] - token['z_line']
            if token['e_line'] > 0 :
                str2 = txt[z_txt:e_txt]
                if not token['match'] == txt[z_txt:e_txt] :
                    print("FALIED!")
                    success = False
                    break
    if success :
        print("PASSED!")


#----------- Z/E_LINE TEST ------------ #
if ze_line_test :
    success = True
    print("...z/e_line_test...",end='')
    lines = txt.splitlines()
    for token in tokens : # verbose
        if token['match'] is not None :
            lineNum = token['line_number']
            e_line  = token['e_line']
            z_line  = token['z_line']

            if token['e_line'] > 0 :
                str2 = lines[lineNum-1][z_line:e_line]
                if not token['match'] == str2 :
                    print("FALIED!")
                    success = False
                    break

    if success :
        print("PASSED!")

#----------- OUTPUT TOKENS AS JSON ------------ #
if OutputTokesnAsJson :
    print("Outputing tokens to '%s'" % TOKENS_OUPUT_PATH )
    write_json(tokens, TOKENS_OUPUT_PATH)
