import sys

def validate_item(item, desired_namestr, desired_item_type, err:bool=False,cnfg=None):

    retu = True
    err_msg = ''
    nmstr,item_type,args = process_item(item,no_res=True)
    res = None

    if nmstr != desired_namestr:
        err_msg+= f"nmstr was '{nmstr}' not '{desired_namestr}'"
        retu = False

    if item_type != desired_item_type:
        head = ""
        if err_msg != "":
            head = " and "
        err_msg+= f"{head} item_type was '{item_type}' not '{desired_item_type}'"
        retu = False

    if not retu and err:
        sys.exit(f"ERROR: Validation Failed for '{item}': {err_msg}")

    if retu:
        res = process_args(nmstr,item_type,args,cnfg=cnfg)


    return retu, res


def process_item(item:str,cnfg=None,no_res=False):
    nmstr     = item
    item_type = get_item_type(item)
    res       = None

    # non-literal
    if item_type != 'ltrl':
        nmstr, args = parse_item(item,item_type)
        if not no_res:
            res = process_args(nmstr,item_type,args,cnfg)
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


def process_args(nmstr:str,item_type:str,args:list,cnfg=None):

    res = []

    if item_type == 'vr':
        for arg in args:
            for ark in arg:
                where = None
                pl    = None
                item = None
            res.append([item,pl,where])
            


    elif item_type == 'op':



        if nmstr == 'in':
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

                    

