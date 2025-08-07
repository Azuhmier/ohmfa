import sys


def is_desired_item(
    item:str,
    desired_namestr:str,
    desired_item_type:str,
    error_on_false:bool=False,
):
    """Determines whether an item matches a desired namestr and itemtype.

    Arg
        item (str): given item.
        desired_namestr (str): the namestring to match against 'item'
        desired_item_type (str): the item type to match against 'item'.
        error_on_false (bool, optional): Exit on no match. Defaults to False.

    Returns:
        bool: result; 'retu'
        _type_: result of item processing; 'res'
    """

    nmstr, item_type, args = process_item(item, no_res=True)

    retu = False
    res = None

    # Generate error message upon no match
    err_msg = ''
    if nmstr != desired_namestr:
        err_msg+= f"'nmstr' was '{nmstr}' not '{desired_namestr}'. "
    if item_type != desired_item_type:
        err_msg+= f"item_type' was '{item_type}' not '{desired_item_type}'."

    # Determine match result based on if 'err_msg' is an empty string.
    if err_msg == "":
        retu = True
        res = process_args(nmstr, item_type, args)
    elif error_on_false:
        sys.exit(f"ERROR: '{item}' is did not match: {err_msg}")

    return retu, res


def process_item(item:str, no_res:bool=False):
    nmstr = None
    item_type = get_item_type(item)
    res = None

    # non-literal
    if item_type != 'ltrl' and item_type !='bool':
        nmstr, args = parse_item(item,item_type)
        if no_res:
            res = args
        else:
            res = process_args(nmstr,item_type,args)
    else:
        nmstr = item
    return nmstr, item_type, res


def parse_item(item, item_type):
    #private method
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
    #private method
    item_type = None
    if isinstance(item, bool):
        item_type = 'bool'
    elif isinstance(item,list):
        item_type = 'ar'
    elif item[0] == '_':
        if item[-1] == '_':
            item_type = 'vr'
        else:
            item_type = 'op'
    else:
        item_type = 'ltrl'
    return item_type


def process_args(nmstr:str,item_type:str,args:list):
    # private method
    res = []
    if item_type == 'vr':
        for arg in args:
            argname = ['varname', 'curr', 'set']
            dres={}
            for ark in arg:
                key = argname.pop(0)
                dres[key] = ark
            res.append(dres)
    elif item_type == 'op':
        if nmstr == 'in':
            res = args
        elif nmstr == 'for':
            res = args
        elif nmstr == 'css':
            res = args
        elif nmstr == 'text':
            res = args
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

                    

