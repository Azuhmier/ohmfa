import sys
sys.path.append("/home/azuhmier/progs/ohmfa/lib")
from ohmfa.main import Main
URLS_FILE = '/home/azuhmier/hmofa/hmofa/.ohm/output/paged_lists/objs/plain/url.txt'

o = Main()
o.load_urls(URLS_FILE)
o.create_fetcher('/home/azuhmier/hmofa/archive')
o.fetcher.start_session()
o.fetcher.fetch_all(max=1)
o.fetcher.delete_all_sessions()
#f = Fetcher('/home/azuhmier/progs/ohmfa/t/scratch/lib/frameworks/domains_config.yml')
#o.urls = test_urls + o.urls
#o.urls = test_urls
#f.load_urls(o.urls,slds=oslds,verbose=1,mx=2,prnt=0)
#f.load_urls(o.urls,verbose=1)
#f.get_passwords('/home/azuhmier/.pwds')
#f.start_session()
#f.check_urls(no_domain=True)
#f.check_urls(slds=oslds)

#f.d.quit()
#f.delete_all_sessions()