"""
CAVEATS:
- All Arrays are of non-zero length
- All Try block items are scalars
- Default lvl 0 delim is '/'
- Default lvl 1 delim is '.'
- Non Default Delim strs must be indicated at beginning of array via "_delim({delim_str})"
- '_try' ops can not be consecutive
- all bp arrays with lvls greater that 0, must contain 2 or more items

MODEL CHARACTERISTICS:
- every array enters "_m()" first and can over go pre processing
- all recrusive rollbacks have a maximum orlo of 0 (last idx of the array)
- all 'r' values are stored and are unique to each recursion or depth as arrays to account for 
  multiple try blocks

"""
import copy

class Obj():

    def __init__(self):
        pass

    def start_recursion(self,bp:list,ar:list):  
        depth = -1
        lvl   = 0
        suc, bp, ar = self._m(bp,ar,depth,[],lvl)
        return [suc,bp,ar]


    def _m(self, bp:list, ar:list, depth:int, idx:list, lvl:int) -> list:

        # _logars() ##############################################
        def _logars(ind,border,header,bp,ar,idx,lvl,depth):

            bp = copy.deepcopy(bp)
            ar = copy.deepcopy(ar)
            c_bp   = bp
            c_ar   = ar

            for n in range(0,lvl,1):
                i = idx[n]
                c_bp   = c_bp[i]
                c_ar   = c_ar[i]

            c_bp[idx[lvl]] = "<<" + str(c_bp[idx[lvl]]) + ">>"
            c_ar[idx[lvl]] = "<<" + str(c_ar[idx[lvl]]) + ">>"

            print(f"{'':>{ind}}{border*40}")
            print(f"{'':>{ind}}{header}")
            print(f"{'':>{ind}}orlo:     {c_idx+1-len(c_ar)}")
            print(f"{'':>{ind}}DPTH:     {depth}")
            print(f"{'':>{ind}}LVL:      {lvl}")
            print(f"{'':>{ind}}IDX:      {idx}")
            print(f"{'':>{ind}}c_idx:    {idx[lvl]}")
            print(f"{'':>{ind}}bp:       {bp}")
            print(f"{'':>{ind}}ar:       {ar}")
            print(f"{'':>{ind}}bp:       {c_bp}")
            print(f"{'':>{ind}}ar:       {c_ar}")

        # _m() ##############################################
        def _r(r,bp,idx):
            retu = False
            nidx = idx
            if r[-1]['e'] is not None and (idx >= r[-1]['e']): 

                rval_len = len(r[-1]['val'])
                bp[r[-1]['e']:r[-1]['e']] = rval_len

                nidx = r[-1]['e'] - 1
                r[-1]['e'] += rval_len
                retu = True
            return retu,nidx


        # _m() ##############################################
        depth += 1        
        suc = False
        r = []

        if len(idx)-1 < (lvl):
            idx.append(-1)

        c_bp  = copy.deepcopy(bp)
        c_ar  = copy.deepcopy(ar)
        for n in range(0,lvl,1):
            i = idx[n]
            c_bp   = c_bp[i]
            c_ar   = c_ar[i]

        if (idx[lvl]+1 < len(c_ar)):

            while(idx[lvl]+1 < len(c_ar)):

                last_match_was_sucessful=False
                idx[lvl] += 1

                _logars(4,'-','START',bp,ar,idx,lvl,depth)

                if (len(c_bp) - idx[lvl]) < 1:
                    suc, idx[lvl] =  _r(r[-1], c_bp,idx[lvl])
                    if suc:
                        continue
                    r.pop(-1)
                    break

                bp_item = c_bp[idx[lvl]]
                item = c_ar[idx[lvl]]

                # Go down a lvl?
                if isinstance(bp_item,list):
                    suc, tbp, tar = self._m(bp,ar,depth,copy.deepcopy(idx),lvl+1)
                    break

                nmstr,item_type,arg_ar =  process_item(item)

                # '_try()' op?
                if item_type == 'op'
                    process_item(item, assert_item=['op','try'])
                    r.append({'val': arg_ar,'e':idx[lvl]})
                    c_bp.pop(idx[lvl])
                    idx[lvl]-= 1
                    continue

                elif item_type == 'vr':
                    pass

                elif item != bp_item:
                    suc,idx = _r(r[-1],c_bp,idx[lvl])
                    if  suc:
                        continue
                    r.pop(-1)
                    break


                if (idx[lvl]+1 < len(c_ar)):
                    if idx[lvl] != (len(c_bp)-1):
                        if (len(c_bp) - idx[lvl]) > 2:
                            if c_bp[idx[lvl] +1] == delim:
                                next_item = bp[idx[lvl] +2]
                                if process_item(next_item, exists=['op','try']):
                                    c_bp.pop(idx[lvl]+1)
                                    idx[lvl] -= 1
                                    continue
                                    


                last_match_was_sucessful=True



        else:
            _logars(4,'-','START',bp,ar,idx,lvl,depth)
        # Go up a lvl
        if lvl > 0 and last_match_was_sucessful:
            nidx = copy.deepcopy(idx) 
            nidx.pop(-1)
            suc, tbp, tar = self._m(bp,ar,depth,nidx,lvl-1)

        _logars(4,'-','FINAL',bp,ar,idx,lvl,depth)
        return [suc, bp, ar]

o = Obj()
arbf   = [10,11,[20,21,[30,31,[40,41]]],11,12,[20,21],13,14,15]
bp     = [10,11,[20,21,[30,31,[40,42]]],11,12,[20,21],13,14,15]
suc, bp, ar = o.start_recursion(bp,arbf)
print('#'*40)
print(bp)
print(ar)
