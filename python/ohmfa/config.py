import sys
from ohmfa.utils.pather import Pather

class Config(Pather):
    """_summary_

    Args:
        Pather (_type_): _description_
    """
    base      = None
    ohmfa_dir = None
    db        = None

    dspt = {
        '_bad_threads' : ['list', 'local','bad_threads.yml'],
        '_start_url'   : ['hash_value', 3, 'local','config.yml','start_url'],
        '_threads'     : ['path_obj', 'db', 'threads'],
    }

    def __init__(self, base=None,ohmfa_dir=None,db=None):
        if base :
            self.base = self.get_dir_obj(base)[0]
        if ohmfa_dir :
            self.ohmfa_dir = self.get_dir_obj(ohmfa_dir)[0]
        if db :
            self.db = self.get_dir_obj(db)[0]

    def resolv_conf(self, conf, uconf) :
        """_summary_
        """


        for k,v in conf.items():
            if uconf and k in uconf:
                conf[k] = uconf[k]
            elif k in self.dspt:
                dspt_value = self.dspt[k]
                type = dspt_value[0]
                arg = dspt_value[1:]
                conf[k] = self.gen_v(type, arg)

            #else:
            #    sys.exit()


    def gen_v(self, value_type, arg):
        retu = None

        if value_type == 'hash_value' :
            pos = arg[0]
            path_segs = arg[1:pos]
            p = self.get_p(path_segs)
            dictionary = self.read(p)
            keys = arg[pos:]

            retu = dictionary
            for key in keys :
                retu = dictionary[key]

        elif value_type == 'path_obj' :
            path_segs = arg
            retu = self.get_p(path_segs)

        elif value_type == 'list' :
            path_segs = arg
            p = self.get_p(path_segs)
            retu = self.read(p)

        else:
            sys.exit()

        return retu
        

    def get_p(self,arg):

        # ------ Ohmfa_dir ------ #
        where = arg[0]

        p = None

        # ------ Ohmfa_dir ------ #
        # - local
        if where in ['local']  :
            p = self.ohmfa_dir.joinpath('.ohmfa',arg[0],self.db, *arg[1:])
        elif where in ['db']  :
            p = self.ohmfa_dir.joinpath(arg[0],self.db, *arg[1:])
        # - global
        elif where in ['gconf']  :
            p = self.ohmfa_dir.joinpath('.ohmfa',*arg)

        # ------ base ------ #
        elif where in ['config']  :
            p = self.base.joinpath(*arg)

        # ------ Other ------ #
        else:
            sys.exit("Error: " + str(where))

        return p
