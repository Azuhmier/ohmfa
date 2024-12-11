import sys

def validate_item(item, desired_namestr, desired_item_type, err:bool=False,cnfg=None,**kwargs):

    retu = True
    err_msg = ''
    nmstr,item_type,args = process_item(item,no_res=True)
    res = None

    if nmstr != desired_namestr:
        err_msg+= f"nmstr was {nmstr} not {desired_namestr}"
        retu = False

    if item_type != desired_item_type:
        head = ''
        if err_msg == '':
            head = ' and '
        err_msg+= f"{head}item_type was {item_type} not {desired_item_type}"
        retu = False

    if not retu and err:
        sys.exit(f"ERROR: Validation Failed,{err_msg}")

    if retu:
        res = process_args(item,item_type,args,cnfg=cnfg,**kwargs)


    return retu, res


def process_item(item:str,cnfg=None,no_res=False,**kwargs):

    nmstr     = item
    item_type = get_item_type(item)
    res       = None

    # non-literal
    if item_type != 'ltrl':
        nmstr, args = parse_item(item,item_type)
        if not no_res:
            res = process_args(nmstr,item_type,args,cnfg,**kwargs)
        else:
            res = args

    return nmstr, item_type, res


def parse_item(item,item_type):
    """_summary_
    """
    args   = None
    nmstr  = None

    if item_type == 'ar':
        args = item 

    else:
        z = item.find('(')
        e = item.rfind(')')
        arg_str =  item[(z+1):e]

        args = arg_str.split('|')
        args = [arg.split(';') for arg in args]
        nmstr = item[1:z]

    return nmstr, args


def get_item_type(item):
    """_summary_
    """

    item_type = None
    if item[0] == '_':
        if item[-1] == '_':
            item_type = 'vr'
        else:
            item_type = 'op'

    elif isinstance(item,list):
        item_type = 'ar'

    else:
        item_type = 'ltrl'

    return item_type


def process_args(nmstr:str,item_type:str,args:list,cnfg=None,**kwargs):

    res = []

    if item_type == 'vr':
        for arg in args:
            for ark in arg:
                where = None
                pl    = None
                item = ark[0]
                if ark[0][0] == '_':
                    res = ark.split('=')
                    if len(res) >= 2:
                        pl = res[1]
                        item = res[0]
                if len(ark) > 1:
                    where = ark[1]
            res.append([item,pl,where])


    elif item_type == 'op':

        if nmstr == 'mi':
                res = []
                if len(args) > 1:
                    sys.exit(f"ERROR: op '{nmstr}' is requires 1 or less args, {len(args)} was supplied")
                elif len(args):
                    if len(args[0]) != 2:
                        sys.exit(f"ERROR: op '{nmstr}' requires 2 subargs, {len(args[0])} was supplied")
                    else:
                        res = cnfg
                        # - m string ---------------
                        # - m
                        m = None
                        m_str = args[0][0]
                        m_e = m_str.find('[')
                        if m_e != -1:
                            m = m_str[:m_e]
                        else:
                            m = m_str
                        # - m query
                        m_query = {}
                        if m_e != -1:
                            m_query_e = m_str.find(']')
                            m_query_str = m_str[m_e:m_query_e]
                            m_query_strs = m_query_str.split(' ')
                            for qstr in m_query_strs: 
                                query = qstr.split('=')
                                if len(query) != 2:
                                    sys.exit(f"ERROR: op '{nmstr}' requires both sides of '=' to be non-none")
                                else:
                                    qkey  = query[0]
                                    qvals = query[0].split(',')
                                    mp = False
                                    if qkey[-1] == '!':
                                        qkey  = query[:-1]
                                        qnot = True
                                        res = {k:v for k,v in res.items() if v[qkey] not in qvals}
                                    else:

                                        if qkey[-1] == '*':
                                            qkey  = query[:-1]
                                            mp = True
                                        
                                        res = {k:v for k,v in res.items() if v[qkey] in qvals}
                                        


                        # i string --------------------
                        # - i
                        i = None
                        i_str = args[0][1]
                        i_e = item.find('[')
                        if i_e != -1:
                            i = i_str[:i_e]
                        else:
                            i = i_str
                        # - i query
                        i_query = {}
                        if m_e != -1:
                            i_query_e = i_str.find(']')
                            i_query_str = i_str[m_e:m_query_e]
                            i_query_strs = i_query_str.split(' ')
                            for qstr in i_query_strs: 
                                query = qstr.split('=')
                                if len(query) != 2:
                                    sys.exit(f"ERROR: op '{nmstr}' requires both sides of '=' to be non-none")
                                else:
                                    qkey  = query[0]
                                    qvals = query[0].split(',')
                                    mp = False
                                    if qkey[-1] == '!':
                                        qkey  = query[:-1]
                                        qnot = True
                                        res = {k:v for k,v in res.items() if v[qkey] not in qvals}
                                    else:

                                        if qkey[-1] == '*':
                                            qkey  = query[:-1]
                                            mp = True
                                        
                                        res = {k:v for k,v in res.items() if v[qkey] in qvals}

                        res = [m,i,res]
                else:
                    res=None

        elif nmstr == 'type':
            retu = None
            for idx,arg in enumerate(args[0]):
                x = None
                if arg == 'list':
                    x = []
                elif arg == 'str':
                    x = ''
                elif arg == 'int':
                    x = 0
                elif arg == 'datetime':
                    x = 0
                elif arg == 'bool':
                    x = 0
                if idx:
                    retu.append(x)
                else:
                    retu = x
            res = retu

        elif nmstr == 'in':
            res = args

        elif nmstr == 'for':
            res = args

        elif nmstr == 'css':
            res = args

        elif nmstr == 'text':
            res = args


        # - try---------------------------
        elif nmstr == 'delim':
            res = args

        elif nmstr == 'try':

            if len(args):
                if len(args) <= 2:

                    max_try = None
                    if len(args) == 2:
                        max_try = args[1][0]
                        max_try = int(max_try)

                    items = args[0]
                    new_items = []
                    vr_seen = False
                    for item in items:
                        nmstr,item_type,args = process_item(item)
                        if item_type == 'vr':
                            if vr_seen:
                                sys.exit(F"ERROR: '_try()' does not support consecutive 'vr' items: {item} ")
                            else:
                                vr_seen = True
                        elif item_type == 'ltrl':
                            vr_seen = False
                        elif item_type == 'op':
                            sys.exit(F"ERROR: '_try()' does not support 'op' items: {item} ")

                        new_items.append(item)

                    res = [new_items,max_try] 

    return res

                    

