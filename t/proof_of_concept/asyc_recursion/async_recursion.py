"""
CAVEATS:
- All Arrays are of non-zero length

MODEL CHARACTERISTICS:
- every array enters "_m()" first and can over go pre processing
- all recrusive rollbacks have a maximum orlo of 0 (last idx of the array)

"""
import copy

class Obj():

    def __init__(self):
        pass

    def start_recursion(self,bp:list,ar:list):  
        depth = 0
        lvl   = 0
        idx   = []
        retu, bp, ar = self._m(bp,ar,depth,idx,lvl)
        return [retu,bp,ar]


    def _m(self, bp_in:list, ar_in:list, depth:int, idx:list, lvl:int) -> list:

        # _logars() ##############################################
        def _logars(ind,border,header,bp,ar,idx,lvl,depth,retu):

            bp = copy.deepcopy(bp)
            ar = copy.deepcopy(ar)
            c_bp   = bp
            c_ar   = ar
            for n in range(0,lvl,1):
                i = idx[n]
                c_bp   = c_bp[i]
                c_ar   = c_ar[i]

            if idx[lvl] < len(c_bp):
                c_bp[idx[lvl]] = "<<" + str(c_bp[idx[lvl]]) + ">>"
            else:
                c_bp[-1] = "((" + str(c_bp[-1]) + "))"

            if idx[lvl] < len(c_ar):
                c_ar[idx[lvl]] = "<<" + str(c_ar[idx[lvl]]) + ">>"
            else:
                c_ar[-1] = "((" + str(c_ar[-1]) + "))"

            print(f"{'':>{ind}}{border*40}")
            print(f"{'':>{ind}}{header}")
            print(f"{'':>{ind+4}}DPTH: {depth} LVL: {lvl} orlo: {idx[lvl]+1-len(c_ar)} retu: {retu}")
            print(f"{'':>{ind+4}}IDX:      {idx}")
            print(f"{'':>{ind+4}}bp:       {bp}")
            print(f"{'':>{ind+4}}ar:       {ar}")

        # _m() ##############################################
        depth += 1        

        if len(idx)-1 < (lvl):
            idx.append(-1)

        bp  = copy.deepcopy(bp_in)
        ar  = copy.deepcopy(ar_in)
        c_bp = bp
        c_ar = ar
        for n in range(0,lvl,1):
            i = idx[n]
            c_bp   = c_bp[i]
            c_ar   = c_ar[i]

        start_idx = idx[lvl] 

        retu = False
        while(idx[lvl] < len(c_ar)):

            idx[lvl] += 1



            if idx[lvl] == start_idx + 1:
                _logars(4,'-','START',bp,ar,idx,lvl,depth,retu)
            else:
                _logars(4,'-','NEXT',bp,ar,idx,lvl,depth,retu)

            if(idx[lvl] >= len(c_ar)):
                break
            elif idx[lvl] >= len(c_bp):
                retu = False
                break

            retu = False

            bp_item = c_bp[idx[lvl]]
            item    = c_ar[idx[lvl]]

            # Go down a lvl?
            if isinstance(bp_item,list):

                retu, new_bp, new_ar = self._m(bp,ar,depth,copy.deepcopy(idx),lvl+1)
                if retu:
                    bp[:] = new_bp
                    ar[:] = new_ar
                break

            #if depth == 3:
            #c_ar[idx[lvl]] = f"{depth}{lvl}{idx[lvl]} wuz here"
            if item != bp_item:
                break
            else:
                retu = True
            


        # Go up a lvl
        if lvl > 0 and idx[lvl] == len(c_ar):
            nidx = copy.deepcopy(idx) 
            nidx.pop(-1)
            retu, new_bp, new_ar = self._m(bp,ar,depth,nidx,lvl-1)
            if retu:
                bp[:] = new_bp
                ar[:] = new_ar

        _logars(4,'-','FINAL',bp,ar,idx,lvl,depth,retu)
        return [retu, bp, ar]



# _m() ##############################################
o = Obj()

bp     = [100,101,[210,211,[320,321]],503,504,[610, 611],706,708]
ar     = [100,101,[210,211,[320,321]],503,504,[610, 611],706,708]
res, bp, ar = o.start_recursion(bp,ar)
print('#'*40)
print(bp)
print(ar)

