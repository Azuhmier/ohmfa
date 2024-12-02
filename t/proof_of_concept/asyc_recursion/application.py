"""
CAVEATS:
- All Try block items are scalars
- Default lvl 0 delim is '/'
- Default lvl 1 delim is '.'
- Non Default Delim strs must be indicated at beginning of array via "_delim({delim_str})"
- '_try' ops can not be consecutive
- all bp arrays with lvls greater that 0, must contain 2 or more items

MODEL CHARACTERISTICS:
- all 'r' values are stored and are unique to each recursion or depth as arrays to account for 
  multiple try blocks
- [x, "x", [x, "x"]] == [x, x, [x, "x"]]

"""

import copy


class UrlPathResolver():

    def __init__(self,verbose=0,prnt=0):
        self.log = []
        self.verbose = verbose
        self.prnt = prnt


    def start_recursion(self, bp:list, ar:list):  
        depth = 0
        lvl   = 0
        idx   = []
        retu, bp, ar = self._m(bp,ar,depth,idx,lvl)
        return [retu,bp,ar]


    def _m(self, bp_in:list, ar_in:list, depth:int, idx:list, lvl:int) -> list:


        # _logars() ##############################################
        def _logars(ind:int, border:str, header:str, bp:list, ar:list, idx:int, lvl:int, depth:int, retu:bool, bp_len:int, r_ar:list) -> None:
            r_e = None
            if len(r_ar):
                r_e = r_ar[-1]['e']
            bp = copy.deepcopy(bp)
            ar = copy.deepcopy(ar)
            c_bp, c_ar = get_cur(idx,lvl,[bp,ar])

            if idx[lvl] < len(c_bp):
                c_bp[idx[lvl]] = "<<" + str(c_bp[idx[lvl]]) + ">>"
            else:
                c_bp[-1] = "((" + str(c_bp[-1]) + "))"

            if idx[lvl] < len(c_ar):
                c_ar[idx[lvl]] = "<<" + str(c_ar[idx[lvl]]) + ">>"
            else:
                c_ar[-1] = "((" + str(c_ar[-1]) + "))"

            if self.verbose:
                print(f"{'':>{ind}}{border*40}")
                print(f"{'':>{ind}}{header}")
                print(f"{'':>{ind+4}}DPTH: {depth} LVL: {lvl} orlo: {idx[lvl]+1-len(c_ar)} bporlo: {idx[lvl]+1-len(c_bp)} orli: {(idx[lvl]+1-(start_idx+1)) - bp_len} bp_len: {bp_len} r_e: {r_e} retu: {retu}")
                print(f"{'':>{ind+4}}IDX:      {idx}")
                print(f"{'':>{ind+4}}ar:       {ar}")
                print(f"{'':>{ind+4}}bp:       {bp}")


        # _r() ##############################################
        def _r(bp,idx,r_ar,bp_len) -> list:
            retu=False
            while(len(r_ar)):
                r = r_ar[-1] 
                if  r['e'] <= idx:
                    bp[r['e']:r['e']] = r['val']
                    idx = r['e']
                    r['e'] += len(r['val'])
                    idx -= 1
                    retu = True
                    bp_len += len(r_ar[-1]['val'])
                    break
                else:
                    bp[:] = r['old_bp'][:]
                    bp_len = r['old_bp_len']
                    r_ar.pop(-1)

            return retu, idx, r_ar, bp_len
            

        # get_cur() ##############################################
        def get_cur(idx,lvl,args) ->list:
            for n in range(0,lvl,1):
                args = [arg[idx[n]] for arg in args]
            return args

        # _m() ##############################################
        # Manual Depth Enumeraton ----------
        depth += 1        

        # Create new index at lvl if none exists ----------
        if len(idx)-1 < (lvl):
            idx.append(-1)

        # Get arrays at current lvl and index ----------
        bp  = copy.deepcopy(bp_in)
        ar  = copy.deepcopy(ar_in)
        c_bp, c_ar = get_cur(idx,lvl,[bp,ar])

        # Manual Depth Enumeraton ----------
        start_idx = idx[lvl] 


        # Virtual BP Length ----------
        bp_len = 0
        for item in c_bp[idx[lvl]+1:]:
            bp_len +=1
            if isinstance(item,list):
                bp_len -=1
                break

        # Loop Variales ----------
        r_ar = []
        retu = False

        # Loop Start ----------
        while(idx[lvl] < len(c_ar)):

            # Manual Enumeration ----------
            idx[lvl] += 1

            # Logging ----------
            if idx[lvl] == start_idx + 1:
                _logars(4,'-','START',bp,ar,idx,lvl,depth,retu,bp_len,r_ar)
            else:
                _logars(4,'-','NEXT',bp,ar,idx,lvl,depth,retu,bp_len,r_ar)

            # AR EXHAUSTION ----------
            if(idx[lvl] >= len(c_ar)):
                if len(c_ar) > len(c_bp):
                    r_res,idx[lvl],r_ar,bp_len = _r(c_bp,idx[lvl],r_ar,bp_len)
                    if r_res:
                        continue
                    else:
                        retu = False
                elif len(c_ar) < len(c_bp):
                    retu=False
                    if idx[lvl] + 1 == len(c_bp):
                        if isinstance(c_bp[idx[lvl]],str):
                            c_bp.pop(idx[lvl])
                            retu = True
                else:
                    retu = True
                break

            # VIRTUAL BP EXHAUSTION ----------
            if idx[lvl] >= len(c_bp):
                r_res,idx[lvl],r_ar,bp_len = _r(c_bp,idx[lvl],r_ar,bp_len)
                if r_res:
                    continue
                else:
                    retu = False
                break

            # This round is now cannon ----------
            retu = False

            # Safe to index ----------
            bp_item = c_bp[idx[lvl]]
            item    = c_ar[idx[lvl]]

            # Go down a lvl? ----------
            if isinstance(bp_item,list):
                ar_copy = copy.deepcopy(ar)
                if not isinstance(item,list):
                    c_ar_copy = get_cur(idx,lvl,[ar_copy])[0]
                    c_ar_copy[idx[lvl]] = [item]
                retu, new_bp, new_ar = self._m(bp,ar_copy,depth,copy.deepcopy(idx),lvl+1)
                if retu:
                    bp[:] = new_bp
                    ar[:] = new_ar
                else:
                    r_res,idx[lvl],r_ar,bp_len = _r(c_bp,idx[lvl],r_ar,bp_len)
                    if r_res:
                        continue
                break

            # BP EXHAUSTION ----------
            elif idx[lvl] +1 -(start_idx+1) > bp_len:
                r_res,idx[lvl],r_ar,bp_len = _r(c_bp,idx[lvl],r_ar,bp_len)
                if r_res:
                    continue
                break

            # - Non-Literals ----------
            elif isinstance(bp_item, str):
                # - variable
                if bp_item[0] == 'v':
                    retu = True
                # - Try Operator
                else:
                  arg_ar = bp_item.split(';')
                  arg_ar1 = [int(x) for x in arg_ar if x[0] != '_']
                  arg_ar2 = [str('v') + x for x in arg_ar if x[0] == '_']
                  arg_ar = arg_ar1 + arg_ar2
                  r = {
                      'e': idx[lvl],
                      'val': arg_ar,
                      'old_bp_len': bp_len,
                      'old_bp': copy.deepcopy(c_bp) }
                  r_ar.append(r)
                  c_bp.pop(idx[lvl])
                  idx[lvl] -= 1
                  bp_len -= 1
                  continue

            # literals ----------
            elif item != bp_item:
                r_res, idx[lvl], r_ar,bp_len = _r(c_bp,idx[lvl],r_ar,bp_len)
                if r_res:
                    continue
                break
            else:
                retu = True

        # Go up a lvl ----------
        if lvl > 0 and idx[lvl] == len(c_ar) and retu:
            nidx = copy.deepcopy(idx) 
            nidx.pop(-1)
            retu, new_bp, new_ar = self._m(bp,ar,depth,nidx,lvl-1)
            if retu:
                bp[:] = new_bp
                ar[:] = new_ar

        # FINAL ----------
        _logars(4,'-','FINAL',bp,ar,idx,lvl,depth,retu,bp_len,r_ar)
        return [retu, bp, ar]

# MAIN ##############################################
o = UrlPathResolver()
test = {
    'basic' : {
      'bp': [],
      'ar': []
    } 
}
#ar     = [100,101,[210,211,[320,321]],503,504,[610, 611],706]
#bp     = [100,101,[210,211,[320,321]],503,"504",[610, 611],706]

#ar     = [100,101,[210,211,[320,321]],503,504,610,706]
#bp     = [100,101,[210,211,[320,321]],503,504,[610, "611"],706]

#ar     = [100,101,[210,211,320],503,504,505,[610, 611],706]
#bp     = [100,101,[210,211,[320,"321"]],"503",504,"505",[610, "611"],706]

#ar     = [100,101,[210,211,320],503,504,505,[610, 611],706]
#bp     = [100,101,["210;211",[320,"321"]],"503",504,"505",[610, "611"],"706"]

#ar     = [100,101,[210,211,320],503,504,505, 610, 706]
#bp     = [100,"v_101_",["210;211",["v_320_","321"]],"503",504,"505",[610, "611"],"706"]

#ar     = [100,101,[210,211,320],503,504,505, 610, 706]
#bp     = [100,"v_101_",["2102;211",["v_320_","321"]],"503",504,"505",[610, "611"],"706"]

#ar     = [100,101,[210,211,211,321,320],503,504,[9, 610],706]
#bp     = ['_100_',101,["209",210,"_211_",["_320_","v_321_"],[320,"_321_"]],503,504,["_9_", ["_610_", 610]],706]

#ar = [1,7,7,4,2,2,[3,4,4]]
#bp = [1,"_7_",4,2,[3,"4"]]
#ar = [    4,2,2]
#bp = ["_7_",4,2]
for k,v in test.items():
    print('#'*40)
    print(k)
    res, new_bp, new_ar = o.start_recursion(v['bp'],v['ar'])
print(res)
print(bp)
print(new_bp)
print(new_ar)