
import re
from ohmfa.fetch.fetcher import Fetcher
from ohmfa.utils.iter import BatchIter, LinkedIter
from ohmfa.utils.pather import SinglePather




class FetchThreads(Fetcher):
    last_fetched_updated = None
    last_fetched         = None
    mode = 'update'

    def __init__(self, **uconf):
        conf = {
            'read_only' : None,
            '_start_url' : None,
            '_bad_threads' : None,
            '_threads' : None,
        }

        self.start_session()
        self.config.resolv_conf(conf,uconf)


        self.threads_dir = conf['_threads']
        self.read_only = conf['read_only']

        # ----- Page Object
        self.page = Page()
        # - LinkedIter
        self.page.iter = conf['_start_url']
        # - Fetcher
        self.page.s = self.s

        # ----- Thread Object
        self.page.thread = Thread()
        self.page.thread.bad_threads = conf['_bad_threads']
        # - SinglePather
        self.page.thread.parent_dir = self.threads_dir
        self.page.thread.fext = '.html'
        # - Fetcher
        self.page.thread.read_only = self.read_only
        self.page.thread.s = self.s

        # ------Last Fetched
        self.last_fetched = self.get_latest_strtime_dir(self.threads_dir)


    def auto(self):
        while self.next():
            pass

    def next(self):
        retu = False
        if self.page.thread.next():
            retu = self.compute()
        elif self.page.next():
            self.page.process()
            if self.page.thread.next():
                retu = self.compute()
            else :
                print('No More Threads!')
                retu = True
        else :
            print('No More Pages!')
            retu = False
        return retu

        

    def compute(self):
        retu = True
        strr = str(str(self.page.iter_idx) + " " + self.page.thread.fname)
        print(strr)

        # redo
        if self.mode =='redo':
            self.page.thread.process()

        # last fetched
        elif self.page.thread.fname == self.last_fetched :
            if not self.last_fetched_updated:
                self.page.thread.process()
                self.last_fetched_updated = True
            elif self.mode == 'update':
                print("Update Done!")
                retu=False
            else :
                print("Already Archived!")

        #Exists
        elif self.page.thread.path.exists():
            #Empty
            if self.page.thread.path.stat().st_size == 0 :
                print("Empty File, Rearchiving!")
                self.page.thread.process()
            else :
                print("Already Archived!")
        # doesn't exists
        else :
            print("Archiving!")
            self.page.thread.process()

        return retu



class Page(Fetcher,LinkedIter):
    thread = None

    def __init__(self):
        LinkedIter.__init__(self)

    def exists_next(self):
        retu = False

        if not self.iter_area:
            self.url = self.iter
            self.fetch()
            self.iter_area = self.soup
        next_button_disabled = self.iter_area.find_all( "li", { "class":re.compile("next disabled") })

        if not next_button_disabled :
            next_button = self.iter_area.find_all( "li", { "class":re.compile("next") })
            self.iter = next_button[0].find("a")["href"]
            self.url = self.iter
            retu=True
        else :
            print("Next Button is Disabled!")
        return retu
        

    def process(self):
        self.iter_procd_idx+=1
        self.fetch()
        op_soups = self.iter_area.find_all( "article", { "class" : re.compile("post doc_id_") })
        self.iter_area = None
        self.thread.iter_area_batch = op_soups




class Thread(Fetcher,BatchIter,SinglePather):
    bad_threads = None

    def __init__(self):
        BatchIter.__init__(self)

    def exists_next(self):
        retu = False
        reply_button = self.iter_area.find( "a", { "title" : "Reply to this post" })
        if reply_button :
            thread_number = reply_button["data-post"]
            self.fname = str(thread_number).strip()
            self.path = self.parent_dir.joinpath(self.fname+self.fext)
            self.iter = reply_button["href"]
            self.url = self.iter
            retu = True
        return retu


    def process(self):
        if not self.bad_threads:
            self.bad_threads = ''
        if not self.fname in self.bad_threads:
            self.iter_procd_idx+=1
            self.fetch()
            if not self.read_only:
                self.write_to_path()
        else :
            if self.path.is_file():
                print("Bad_Thread! Removing from Archive!")
                if not self.read_only:
                    self.path.unlink()
            else:
                print("Bad_Thread! Skipping!")



