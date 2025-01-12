"""_summary_
"""
class Ohmfa:
    """_summary_
    """

    verbose: False
    prnt:    False
    dcnfg: {}


    def __init__(self,verbose=0,prnt=0):
        """_summary_
        """
        self.log=[]
        self.verbose=verbose
        self.prnt=prnt


    def logthis(self, lvl, string):
        """_summary_

        Args:
            lvl (_type_): _description_
            string (_type_): _description_
        """
        if self.verbose >= lvl:
            self.log.append(string)
            if self.prnt :
                print(string)


    def dump(self):
        """_summary_
        """
        for line in self.log:
            print(line)