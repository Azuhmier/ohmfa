"""_summary_
"""
from .ohmfa import Ohmfa

class CnfgProcessor(Ohmfa):
    """_summary_
    """
    def __init__(self,cnfg,verbose=0,prnt=0):
        """_summary_
        """
        super().__init__(verbose,prnt)
        self.cnfg = cnfg
    

    def process_item(self,item):
        """_summary_

        Args:
            item (_type_): _description_

        Returns:
            _type_: _description_
        """
        nmstr     = item
        item_type = self.get_item_type(item)
        arg_ar    = None

        # non-literal
        if item_type != 'ltrl':
            nmstr, arg_ar = self.parse_item(item,item_type)

        return nmstr, item_type, arg_ar


    def parse_item(self,item,item_type):
        """_summary_
        """
        arg_ar = []
        nmstr  = None
        z = item.find('(')
        if z:
            e   = item.rfind(')')
            arg_str =  item[(z+1):e]
            arg_ar  = arg_str.split(';')
            nmstr = item[1:z]
        else:
            if item_type == 'vr':
              nmstr = item[1:-1]
            elif item_type == 'op':
              nmstr = item[1:]
        return nmstr, arg_ar
    def get_item_type(self,item):
        """_summary_
        """
        item_type = None
        if item[0] == '_':
            if item[-1] == '_':
              item_type = 'vr'
            else:
              item_type = 'op'
        else:
            item_type = 'ltrl'
        return item_type


    def process_vr(self,vrnm:str,args:list):
        """_summary_

        Args:
            vrnm (str): _description_
            args (list): _description_
        """


    def process_op_routine(self,opnm:str,arg_ar:list):
        """_summary_

        Args:
            opnm (str): _description_
            arg_ar (list): _description_

        Returns:
            _None_: _description_
        """


    def get_op_ar_val(self,opnm:str,arg_ar:list) -> list:
        """_summary_

        Args:
            opnm (str): _description_
            arg_ar (list): _description_

        Returns:
            _type_: _description_
        """


    def get_op_str_val(self,opnm:str,arg_ar:list) -> str:
        """_summary_

        Args:
            opnm (str): _description_
            arg_ar (list): _description_

        Returns:
            _type_: _description_
        """