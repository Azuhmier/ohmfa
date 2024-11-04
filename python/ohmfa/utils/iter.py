"""iter.py"""




from ohmfa.ohmfa import Ohmfa




class Iter(Ohmfa):
    # Iter Vars
    iter_idx         = 0
    iter_procd_idx   = 0
    iter             = None
    iter_area        = None



    def __init__(self):
        pass


    def next(self):
        ret = False
        if self.get_next() :
            self.iter_idx+=1
            ret = True
        return ret


    def get_next(self):
        return False
    def exists_next(self):
        return False



    def process(self):
        pass




class BatchIter(Iter):
    iter_batch = None
    iter_area_batch = None


    def __init__(self, iter_batch=None, iter_area_batch=None):
        self.iter_batch = iter_batch
        self.iter_area_batch = iter_area_batch


    def get_next(self):
        retu = None

        if self.iter_batch:
            self.iter = self.iter_batch.pop()
            retu = self.exists_next()
        elif self.iter_area_batch:
            self.iter_area = self.iter_area_batch.pop()
            retu = self.exists_next()
            
        return retu




class LinkedIter(Iter):
    

    def __init__(self, start_iter=None, iter_area=None):

        self.iter           = start_iter
        self.iter_area      = iter_area


    def get_next(self):
        retu = False
        retu=self.exists_next()
        return retu
