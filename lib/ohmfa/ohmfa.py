##MASTER
class Ohmfa:
    verbose = False
    prnt =    False
    dcnfg = {}


    def __init__(self,verbose=0,prnt=0):
        self.log=[]
        self.verbose=verbose
        self.prnt=prnt


    def logthis(self, lvl, string):
        if self.verbose >= lvl:
            self.log.append(string)
            if self.prnt :
                print(string)


    def dump(self):
        for line in self.log:
            print(line)