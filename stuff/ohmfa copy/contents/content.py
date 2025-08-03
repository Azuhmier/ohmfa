class Content(Contents,BatchIter):
    url = None
    bad_urls = None
    domain_key = None
    o = None
    wfl = None
    wfl_name = None
    running = False
    Triggered = False
    strtime = None
    fetcher = None
    
    def __init__(self,read_only):
        """_summary_
        """
        self.read_only = read_only
        pather_opts = {
            'ptype': 'file',
            'read_only':read_only
        }
        self.meta = SinglePather(pname='meta.json',**pather_opts)
        self.scrape = SinglePather(**pather_opts)

    def next_exists(self):
        """_summary_
        """
        self.strtime = self.iter
        self.o = urlparse(self.url)
        self.fetcher.get_domain_config()
        self.fetcher.vars['url'] = self.url
        self.fetcher.vars['ua'] = self.ua
        self.fetcher.vars['domain'] = self.o.netloc
        return True


    def process(self):
        """_summary_
        """
        self.scrape.write()
        self.meta.write()