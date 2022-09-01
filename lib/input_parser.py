import re
import sys
import copy


DefaultTokenParams = {
        'enabled' : False ,
        'uid'     : None,
        'name'    : None ,
        'ed_enbl' : [] ,
        'ed_dsbl' : [] ,
        'ed_optnl' : False ,
        'sc'      : [] ,
        'sc_en'   : False ,
        'f_prty'  : False ,
        'f_eolt'  : False ,
        'f_optnl' : False ,
        'f_grdy'  : False ,
        'f_give'     : False ,
        'f_c'     : False ,
        'cnt'     : [0,0,0],
        'max'     : [None,None,None] ,
}

pats = {
    'TokDef'         : re.compile( '(?x)  ^\s*([A-Za-z0-9_-]+)\s* /((?: (?<=\\\)/|[^/] )*)/ \s* (?:/((?: (?<=\\\)/|[^/] )*)/)* \s* (?: \((.*)\) )? $' ),
    'TokObj'         : re.compile( '^(\s*)([^ -][A-Za-z0-9_-]+)\s*(?:@\s*([A-Za-z0-9_-]+))?\s*$' ),
    'ed'             : re.compile( '^(\s*)([-~])(\?)?', ),
    'sc'             : re.compile( '^(\s*)(<|>)(!)?' ),
    'opt'            : re.compile( '^\s*\$([A-Za-z0-9_-]+)\s*=\s*(.*)' ),
}



def parse_input(user_input, opts) :
    global pats
    global DefaultTokenParams
    lines      = user_input.splitlines()
    pntr       = []
    tabstop    = None
    lvl_buffer = [None, None]
    TokObjs  = {}
    TokDefs  = {}
    for line in lines:
        for argtype in pats.keys() :
            m = pats[argtype].match(line)
            if m :

                ## STATIC
                if argtype == 'TokDef' :
                    dname       = m.group(1)
                    pat1        = m.group(2)
                    pat2        = m.group(3)
                    ArgSwitches = m.group(4)
                    TokDefs[dname] = copy.deepcopy(DefaultTokenParams)
                    if len(pat1) == 0 :
                        pat1 = None
                        TokDefs[dname]['f_c'] = True
                    if pat2 is not None and len(pat2) == 0 :
                        TokDefs[dname]['f_eolt'] = True
                    TokDefs[dname]['name'] =  dname
                    TokDefs[dname]['pat1'] = pat2
                    TokDefs[dname]['pat2'] = pat1
                    if ArgSwitches is not None :
                        ArgSwitches = ArgSwitches.strip()
                    if ArgSwitches is not None and len(ArgSwitches) :
                        ArgSwitchesList = ArgSwitches.split('-')
                        if len(ArgSwitchesList) > 1 :
                            ArgSwitchesList = ArgSwitchesList[1:]
                        for argswitch in ArgSwitchesList:
                            argswitch.rstrip()
                            argswitchParts = argswitch.split(' ')
                            if argswitchParts[-1] == '' :
                                argswitchParts = argswitchParts[:-1]
                            if not len(argswitchParts) > 1 :
                                sys.exit('ERROR:dsafd')
                            argv_list = argswitchParts[1].split(',')
                            arg_flag = argswitchParts[0]
                            if arg_flag != 'max' :
                                TokDefs[dname][arg_flag] = int(argv_list[0])
                            else:
                                for idx, argv in enumerate(argv_list) :
                                    if argv :
                                        TokDefs[dname][arg_flag][idx] = int(argv)
                ## VOLATILE
                elif argtype in ['TokObj','sc','ed'] :
                    LeadingWhiteSpace =  m.group(1)
                    if tabstop is None :
                        tabstop = len(LeadingWhiteSpace)
                        if tabstop not in [2, 4] :
                            sys.exit('ERROR: tabstop %d is invalid, tabstop must be either 2 or 4' % tabstop)
                    tabN = len(LeadingWhiteSpace)/tabstop
                    UID = None
                    if argtype == 'TokObj' :
                        dname = m.group(2)
                        uname = m.group(3)
                        lvl_buffer[0] = lvl_buffer[1]
                        lvl_buffer[1] = int(tabN)
                        if lvl_buffer[0] is None :
                            lvl_buffer[0] = 0
                        diff = lvl_buffer[1] - lvl_buffer[0]
                        TokObj = copy.deepcopy(TokDefs[dname])
                        if uname :
                            TokObj['name'] = uname
                        if diff == 1 :
                            pntr.append(0)
                        elif diff < 0 :
                            for i in range(int(diff*-1)) :
                                pntr.pop()
                            pntr[-1] += 1
                        elif diff == 0 :
                            pntr[-1] += 1
                        elif diff > 1 :
                            sys.exit('ERROR: 199')
                        UID_str = [str(i) for i in pntr]
                        UID = '.'.join(UID_str)
                        TokObj['uid'] = UID
                        TokObjs[UID] = TokObj
                    else :
                        UID = argtype
                    check(argtype, m, TokObjs, lvl_buffer, UID, tabstop)
                elif argtype == 'opts' :
                    opt = m.group(1)
                    value = m.group(2)
                    OhmfaOpts[opt] = value
    return TokObjs
def check(argtype, m, TokObjs, lvl_buffer, UID,  tabstop): #{{{
    global OhmfaOpts
    if not hasattr(check, 'pot'):
        check.pot = {
            'ed'     : { 0 : [0, None, [], None] },
            'sc'     : { 0 : [0, [], None] },
            'TokObj' : { 0 : [0, None, []] }
        }
        check.prev = [['', -1]]
    LeadingWhiteSpace =  m.group(1)
    tabN = len(LeadingWhiteSpace)
    if argtype != 'TokObj' :
        lvl = int(tabN/tabstop)
    else:
        lvl  = lvl_buffer[1]
    plvl = lvl_buffer[0]
    diff = lvl_buffer[1] - lvl_buffer[0]
    if argtype == 'sc' :
        bracket = m.group(2)
    if argtype != 'TokObj' :
        if diff > 1 :
            sys.exit('ERROR: 233')
        if diff < 0 :
            if check.prev[-1][1] > lvl :
                sys.exit('ERROR: 237')
    if lvl not in check.pot['ed'].keys() :
        check.pot['ed'][lvl] = copy.deepcopy(check.pot['ed'][0])
    if plvl not in check.pot['ed'].keys() :
        check.pot['ed'][plvl] = copy.deepcopy(check.pot['ed'][0])
    edt  =  check.pot['ed'][lvl]
    if lvl not in check.pot['sc'].keys() :
        check.pot['sc'][lvl] = copy.deepcopy(check.pot['sc'][0])
    if plvl not in check.pot['sc'].keys() :
        check.pot['sc'][plvl] = copy.deepcopy(check.pot['sc'][0])
    sct  =  check.pot['sc'][lvl]
    if lvl not in check.pot['TokObj'].keys() :
        check.pot['TokObj'][lvl] = copy.deepcopy(check.pot['TokObj'][0])
    if plvl not in check.pot['TokObj'].keys() :
        check.pot['TokObj'][plvl] = copy.deepcopy(check.pot['TokObj'][0])
    lext  =  check.pot['TokObj'][lvl]
    if argtype == 'TokObj' and check.prev[-1][0] == 'sc' and check.pot['sc'][ check.prev[-1][1] ][0] :
        if lvl != check.prev[-1][1] :
            sys.exit('ERROR: 265')
    if argtype == 'ed' and check.prev[-1][1] != lvl :
        sys.exit('ERROR: 269')
    if argtype == 'TokObj' and diff < 0 :
        check.pot[argtype][plvl][0] = 0
        check.pot[argtype][plvl][2] = []
    if edt[0] :
        enabled = None
        if sct[0] and argtype == 'sc' and m.group(2) == '>' :
            enabled = sct[1]
        elif lext[0] and argtype == 'TokObj' and not sct[0] :
            enabled = [ UID ]
        if enabled is not None :
            edt      =  check.pot['ed'][lvl]
            char     = edt[1]
            enablers = edt[2]
            for UID_e in enablers :
                TokObjs[UID_e]['ed_enbl'] = copy.deepcopy( enabled )
            for UID_d in enabled :
                TokObjs[UID_d]['enabled'] = False
                if char ==  '-' :
                    TokObjs[UID_d]['ed_dsbl'] = copy.deepcopy( enablers)
            if edt[3] is not None :
                for UID_e in enablers :
                    TokObjs[UID_e]['ed_optnl'] = True
            edt[0] = 0
            edt[3] = None
    if sct[0] and argtype == 'sc' and m.group(2) == '>':
        for UID_s in sct[1] :
            if sct[2] is not None :
                TokObjs[UID_s]['sc_en'] = True
            TokObjs[UID_s]['sc'] = copy.deepcopy( sct[1] )
        sct[0] = 0
        sct[1] = []
    if argtype == 'TokObj' and diff > 0 :
        lext[0] = 1
        lext[1] = UID
    if not edt[0] and not sct[0] and lext[0] and argtype == 'ed' :
        edt[0] = 1
        token = TokObjs[lext[1]]
        enablers = None
        if token['sc_en']:
            enablers = token['sc']
        else :
            enablers = [ token['uid'] ]
        edt[1] = m.group(2)
        edt[2] = copy.deepcopy( enablers )
        edt[3] = m.group(3)
    if not sct[0] and argtype == 'sc' and m.group(2) == '<' :
        sct[0] = 1
        sct[2] =  m.group(3)
    if sct[0] and argtype == 'TokObj' and check.pot['sc'][lvl][0] :
        token = TokObjs[UID]
        sct[1].append(UID)
    if argtype == 'TokObj' :
        lext[1] = UID
        lext[2].append(UID)
    check.prev.append([argtype, lvl])
