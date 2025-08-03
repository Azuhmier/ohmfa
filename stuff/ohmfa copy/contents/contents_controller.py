"""contents_controller.py
"""
from urllib.parse import urlparse
from ohmfa.contents.contents_fetcher import ContentsFetcher
from ohmfa.utils.pather import Pather, SinglePather
from ohmfa.utils.iter import BatchIter
from ohmfa.ohmfa import Ohmfa




class ContentsController(Contents):

    fetcher = None

    def __init__(self, **uconf):

        conf = {
            'read_only' : None,
            '_contents_bps': None,
            '_contents_db' : None,
            '_bad_urls' : None,
            '_urls' : None,
        }
        self.config.resolv_conf(conf,uconf)
        self.read_only = conf['read_only']
        self.bp        = conf['_contents_bps']
        self.pcwd      = conf['_contents_db']

        # ----- Sinlge Pathers
        archive_opts = {
            'read_only': self.read_only,
            'pdir' : self.pcwd,
        }
        self.pmeta   = SinglePather(pname='meta.json',**archive_opts)
        self.pconfig = SinglePather(pname='config.yml',**archive_opts)
        self.plists  = SinglePather(pname='lists.json',**archive_opts)
        self.plog    = SinglePather(pname='content.log',**archive_opts)

        # ----- UrlDir Object
        self.url_dir       = UrlDir(self.read_only)
        url_dir            = self.url_dir
        url_dir.pcwd       = self.pcwd.joinpath('archive')
        url_dir.url_dirs   = list(url_dir.pcwd.iterdir())
        url_dir.bad_urls   = conf['_bad_urls']
        url_dir.urls       = conf['_urls']

        # ----- Content Object
        content                = url_dir.content
        content.bad_urls       = conf['_bad_urls']
        content.read_only      = conf['read_only']


    def check_env (self) :
        content = self.url_dir.content
        url_dir = self.url_dir
        for url_dir in self.url_dir.url_dirs :
            self.url_dir.next()
            self.lists.pdata["domains"].append(url_dir.o.netloc)
            self.lists.pdata["urlpaths"].append(url_dir.url)
            url_dir.meta.pdata["domain"] = url_dir.o.netloc
            url_dir.meta.pdata["urlpath"] = url_dir.url
            self.url_dir.process()
            content.url = url_dir.url
            for strtimes in url_dir.iter_dir() :
                if strtimes not in ["config.yml", "meta.json", "lists.json"]:
                    content.from_scrape(scrape)
                    url_dir.meta.pdata["codes"].append(content.meta.pdata["code"])
                    self.meta.pdata["size"] = self.meta.pdata["size"] + content.meta.pdata["size"]
                    self.meta.pdata["total_files"] = self.meta.pdata["total_files"] + 1
            if url_dir.list.data["codes"][-1] != "200" :
                self.lists["failed"].append(urlpath)
                if  content.meta.data["domain"] == "archiveofourown.org" :
                    content.meta.data["state"] = "deleted"
                else :
                    content.meta.data["state"] = "error"
        self.lists.data["domains"] = list(set(self.lists.data["domains"]))
        self.meta.data["failed"] = len(self.lists.data["failed"])
        self.meta.data["total_url_paths"] = len(self.lists.data["urlpaths"])
        self.meta.data["total_domains"] = len(self.lists.data["domains"])

    def check_env (self) :
        for urlpath in self.url_dir.parent_dir.iterdir() :
            url_dir = self.url_dir
            content = self.url_dir.content
            url_dir.from_urlpath(urlpath)
            domain = self.url_dir.o.netloc
            url = self.url_dir.url
            self.lists.data["domains"].append(domain)
            self.lists.data["urlpaths"].append(url)
            url_dir.meta.data["domain"] = domain
            url_dir.meta.data["urlpath"] = url
            for scrape in url_dir.iter_dir() :
                if scrape.name not in ["config.yml", "meta.json", "lists.json"]:
                    content.from_scrape(scrape)
                    url_dir.meta.data["codes"].append(content.meta.data["code"])
                    self.meta.data["size"] = self.meta.data["size"] + content.meta.data["size"]
                    self.meta.data["total_files"] = self.meta.data["total_files"] + 1
            if url_dir.list.data["codes"][-1] != "200" :
                self.lists["failed"].append(urlpath)
                if  content.meta.data["domain"] == "archiveofourown.org" :
                    content.meta.data["state"] = "deleted"
                else :
                    content.meta.data["state"] = "error"
        self.lists.data["domains"] = list(set(self.lists.data["domains"]))
        self.meta.data["failed"] = len(self.lists.data["failed"])
        self.meta.data["total_url_paths"] = len(self.lists.data["urlpaths"])
        self.meta.data["total_domains"] = len(self.lists.data["domains"])


    def load_fetcher(self, **conf):
        self.url_dir.content.fetcher = ContentsFetcher(**conf)



    def auto_check(self):
        while self.url_dir.next:
            while self.url_dir.content.next():
                self.url_dir.content.process()
            self.url_dir.process()
        self.process()


    def load_urls(self, urls):
        self.url_dir.content.set_iter_batch(urls)


    def load_archive(self):
        url_dirs = list(self.url_dir.meta.pdir.iterdir())
        self.url_dir.content.set_iter_area_batch(url_dirs)


    def next(self):
        self.url_dir.next()
        self.url_dir.content.next()




