class UrlDir(Contents,BatchIter):
    """_summary_
    """
    url = None
    urls = None
    url_dirs = None
    bad_urls = None
    url_dir = None

    def __init__(self,read_only):
        self.read_only = read_only
        pather_opts = {
            'read_only': read_only
        }
        self.meta    = SinglePather(pname='meta.json',**pather_opts)
        self.list    = SinglePather(pname='list.json',**pather_opts)
        self.config  = SinglePather(pname='config.yml',**pather_opts)
        self.content = Content(read_only)

    def exists_next(self):
        retu = False
        if self.iter_area:
            self.iter = self.get_url_from_url_dir(self.iter_area)
            self.url = self.iter
            retu = True
        else: 
            self.url = self.iter
            retu = True
        
        return retu

    def process(self):
        pdir = self.pcwd.joinpath(self.url_dir)
        self.meta.pdir    = pdir
        self.config.pdir  = pdir
        self.list.pdir    = pdir
        self.content.pcwd = pdir
        self.content.url = self.url
        self.content.iter_batch = self.get_strtimes()
