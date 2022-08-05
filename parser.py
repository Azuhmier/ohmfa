# ============================================================
#
# File:    parser.py
#
# Usage:   ./parser.py
#
# Date:    Thu 08/04/22 13:45:52
# Version: 1.0
# Project: ohmfa
# Author:  Azuhmier (aka taganon), azuhmier@gmail.com
#
# Description:
# ============================================================

#--------------------
#DOC #{{{1
#--------------------
pod = """
===============================
== Parsing Limits ==

\n>{title}\n
\n>{title} ({attrs1})\n
\n>{title} ({attrs1})({attr2})\n

R1) ^\s*>\s*[^ ]+
R2) \s+\(
R2) \)\s*$

P1) {title} can contain '(' & ')'
P2) {attrs1} and {attrs2} can contain '(' & ')'
P3) there will be mistakes
Q1: Is there a way to validate and seperate the {title} from both {attrs1} and {attrs2} in all cases?
    A: NO
Q2: If not, in then what are the cases where one can?

Q3: Can we implement some feedback/UI/GUI/Analysis than can assist a user in cases that one can't?


S1 for P1, assuming P2 doesn't exists: Shotgun method
S2 for P2: Futhrest Method
    0101010101000101011010
     r                  l
    0101010100010101101
    s1s2s3s4  s5s6s7
    9 1's
    10 0's


"""
