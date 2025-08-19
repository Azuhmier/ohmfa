import sys
sys.path.append("/home/azuhmier/progs/ohmfa/lib")
from ohmfa.main import Main
URLS_FILE = '/home/azuhmier/hmofa/hmofa/.ohm/output/paged_lists/objs/plain/url.txt'

o = Main(log_level=10)
o.load_urls(URLS_FILE)
o.create_fetcher('/home/azuhmier/hmofa/archive')
o.fetcher.start_session()
o.fetcher.fetch_all(max=1)
o.fetcher.delete_all_sessions()
o.fetcher.d.quit()