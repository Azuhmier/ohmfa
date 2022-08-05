# ============================================================
#
# File:    lexer.py
#
# Usage:   ./lexer.py
#
# Date:    Thu 08/04/22 10:12:17
# Version: 1.0
# Project: ohmfa
# Author:  Azuhmier (aka taganon), azuhmier@gmail.com
#
# Description:
# ============================================================
#--------------------
#PRESETS {{{1
#--------------------
import sys
import pprint
import re
import copy
pp = pprint.PrettyPrinter(indent=4,sort_dicts=True, width=8)

#--------------------
#SUBS {{{1
#--------------------
def compile_lexer_dspt(lexer_dspt): #{{{2
    for lexer_class in lexer_dspt.values():
        for group in lexer_class:
            for j,atom in enumerate(group):
                group[j] = re.compile(atom)




def lexer(lexer_dspt, lexer_class, txt): #{{{2
    tokens = []
    pats = lexer_dspt[lexer_class]
    group = 0
    order = 0
    z = 0
    e = 1
    txt_len = len(txt)
    txt = txt + '\0'

    _CNT =[0,0,0] # DEBUG
    while e <= txt_len :
        _CNT[0] += 1 # DEBUG

        for order, pat in enumerate(pats[group]) :
            _CNT[1] += 1 #DEBUG
            token = pat.search(txt[z:e])

            if token :
                prev_s1 = token.span()[1] - token.span()[0]
                z += token.span()[0]

                e += 1
                if e > txt_len:
                    prev_s1 = 0

                token = pat.search(txt[z:e])
                while token.span()[1] != prev_s1 :
                    _CNT[2] += 1 # DEBUG

                    e += 1

                    if e > txt_len:
                        break

                    prev_s1 = token.span()[1]
                    token = pat.search(txt[z:e])

                if len(tokens) == 0 or tokens[-1][0] != group or tokens[-1][1] != order:
                    tokens.append([None, None, None])
                    tokens[-1][0] = group
                    tokens[-1][1] = order
                    tokens[-1][2] = []

                tokens[-1][2].append([None, None, None])
                tokens[-1][2][-1][0] = token[0]
                tokens[-1][2][-1][1] = z
                tokens[-1][2][-1][2] = z + token.span()[1]
                z += token.span()[1]
                break
        e += 1

    ## DEBUG
    for i in tokens:
        print(i)
    return tokens
    print(_CNT)
    print(sum(_CNT,0))
    print(sum(_CNT,0)/txt_len)

    return tokens


#--------------------
#MAIN {{{1
#--------------------
lexer_dspt = {
   'author_line': [['\n>']],
   'author_region': [['>[^ ]+','\(','\)','`']],
   'section_line': [['\n%']],
   'section_region': [['%+','[^% ]+']],
   'section': [['%+', '\n', '[^% ]+']],
}

txt = """
%%% s %%%
    %%% s %%%     
    % %% s % %%     


    % %%  % %%     
    %s  %%  % 2%%     
    % %%s% %%     
    %%% s d 43 %%%     
    % %% s d 45  % %%     
    % %%  % %%     
    %s  %%  % dd 2%%     
    % %%s4d% %%     
"""
txt2 = " " * 200000


compile_lexer_dspt(lexer_dspt)
tokens = lexer(lexer_dspt, 'section', txt)

#--------------------
#DOC #{{{1
#--------------------
pod = """
===============================
== TERMS ==
txt buffer, z, e
span, s, s1, s2
lexical analysis
regular expression
context free grammar
token
group
order

===============================
== LEXER_WORKFLOW ==

    START, AND CHECK FOR MATCH
    -------------
    0 1 2 3 4 5 6 E
    z e

    IF NO MATCH EXSTEND STRING, AND CHECK FOR MATCH
    1) e += 1
    -------------
    0 1 2 3 4 5 6 E
    z   e
      m
      s s


    MATCH FOUND, TIGHTEN SELECTION
    1) z += s0, move s0 places foward
    -------------
    0 1 2 3 4 5 6 E
      z e
      m
      s s


    EXSTEND STRING, AND CHECK IF MATCH CONTINUES
    1) e += 1
    -------------
    0 1 2 3 4 5 6 E
      z   e
      m m
      s   s


    MATCH FOUND. EXSTEND STRING, AND CHECK IF MATCH CONTINUES
    1) e += 1
    -------------
    0 1 2 3 4 5 6 E
        z     e
        m m
        s   s

    1) e += 1

    NO FURTHER MATCHES, COUNTIUE TO SEARCH FOR NEXT MATCH
    1) z += s1
    -------------
    0 1 2 3 4 5 6 E
            z e
        m m
        s   s

    NO MATCH FOUND, EXSTEND STRING
    1) e+=1
    -------------
    0 1 2 3 4 5 6 E
              z   e

    NO MORE STRING LEFT
    1) e+=1
    -------------
    0 1 2 3 4 5 6 E
              z     e

"""
