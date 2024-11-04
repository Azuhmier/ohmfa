from ohmfa.ohmfa import Ohmfa
from ohmfa.fetch.fetch_threads import FetchThreads
from pathlib import Path


class Main(Ohmfa) :
    """_summary_
    """

    jobs=[]


    def __init__(self, base=None, ohmfa_dir=None, db=None):
        self.config.base=Path('/home/azuhmier/progs/ohmfa')
        self.config.ohmfa_dir=Path(ohmfa_dir)
        self.config.db='hmofa'


    def fetch(self, fetch_type, **opts) :
        if fetch_type == 'threads' :
            job = FetchThreads(**opts)
            self.jobs.append(job)