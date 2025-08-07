### MASTER
import os
import csv
import sys
import json
import time
import yaml
import pprint

from bs4 import BeautifulSoup
import requests
from seleniumbase import SB
from seleniumbase import Driver

class Fetcher():


    s = None
    s_url = None
    s_fs_timeout = None
    def __init__(self, dcnfg, archive_path=None):
        self.durls = {}
        self.pwds = {}
        self.fs_domains = []
        self.cookie_jar = {}
        self.dspt = dcnfg
        self.archive_path = archive_path


    def start_session(self):

        # --------- request
        self.s = requests.session()
        self.s_url = "http://localhost:8191/v1"
        self.s_fs_timeout = 6000

        # --------- fs
        cmd = "sessions.create"
        headers = {"Content-Type": "application/json"}
        fs_data = { "cmd": cmd}
        r=self.s.post(self.s_url, headers=headers, json=fs_data)
        response_data = json.loads(r.content)
        r = self.s_fs('https://www.google.com')
        response_data = json.loads(r.content)
        user_agent = response_data["solution"]["userAgent"]

        # --------- driver
        self.d = SB(
            uc=True,
            uc_cdp_events=True,
            agent=user_agent,
            headless=True,
            browser="chrome",
            #do_not_track=True,
            #undetectable=True,
            )
        downloads_folder = "/home/azuhmier/progs/ohmfa/dl"  # Specify your desired path


    def delete_all_sessions(self):
        self.d.quit()
        cmd     = "sessions.list"
        headers = {"Content-Type": "application/json"}
        fs_data = { "cmd": cmd}
        r = self.s.post(self.s_url, headers=headers, json=fs_data)
        fs_r_json     = json.loads(r.content)
        session_list = fs_r_json['sessions']
        for session_id in session_list:
            cmd     = "sessions.destroy"
            headers = {"Content-Type": "application/json"}
            fs_data = { "cmd": cmd,"session":session_id}
            r = self.s.post(self.s_url, headers=headers, json=fs_data)
            fs_r_json     = json.loads(r.content)
            status = fs_r_json['status']
            print(f"delete all sessions: {status}")


    def fetch_all(self, start=0, max=0):

        for cnt,durl in enumerate(self.durls):

            if durl.sld != 'archiveofourown':
                max = max + 1
                continue
            if durl.node_type != 'work':
                max = max + 1
                continue

            u = durl.url.geturl()
            u_dname = u.replace("/","_")
            u_dir = os.path.join(self.archive_path,u_dname)
            os.makedirs(u_dir, exist_ok=True)
            u_fname = str(int(time.time()))
            u_path = os.path.join(u_dir,u_fname)

            print(f"{cnt}: {u}")
            #with open(u_path, 'w') as file:
            #    file.write(u_content)
            self.fetch(durl)
            if max and max == cnt:
                break


    def fetch(self,u):
        r  = None
        page_title = None
        fs_cookies = None
        fs_page_title = None
        bad_page_titles = [
            'Reddit - Dive into anything',
            'Fiction.live',
        ]
        # ------- FlareSolverr
        if u.dmn not in self.fs_domains:

            self.fs_domains.append(u.dmn)
            fs_r = self.s_fs(u.url.geturl())
            fs_r_json = json.loads(fs_r.content)
            fs_cookies = fs_r_json["solution"]["cookies"]
            fs_soup = BeautifulSoup(fs_r.content,'html.parser')

            # - update driver
            fs_cookies = sorted(fs_cookies, key=lambda d: d['name'])
            self.d.execute_cdp_cmd('Network.enable',{})
            for fs_cookie in fs_cookies:
                fs_cookie.update({'domain': u.dmn})
                res = self.d.execute_cdp_cmd('Network.setCookie', fs_cookie)
            self.d.execute_cdp_cmd('Network.disable', {})

            # - page title check
            try:
                fs_page_title = fs_soup.head.title.text
                if not fs_page_title:
                    raise(AttributeError)
                elif page_title in bad_page_titles:
                    raise(AttributeError)
            except AttributeError: 
                print('        Bad fs_Title: ', fs_page_title)
            else:
                print('        fs_Title: ', fs_page_title)

        # -------- Driver
        self.d.get(u.url.geturl())
        time.sleep(5)
        cookies = self.d.get_cookies()
        cookies = sorted(cookies, key=lambda d: d['name'])
        # page title check
        try :
            page_title = self.d.title
            if not page_title:
                raise(Exception)
            elif page_title in bad_page_titles:
                raise(Exception)
        except Exception:
            print('        Bad Page_Title: ', page_title)
        else:
            print('        Page_Title: ', self.d.title)
        cks_dict = {cookie['name']: cookie['value'] for cookie in cookies}
        if u.dmn not in self.cookie_jar:
            self.cookie_jar[u.dmn] = {}
        self.cookie_jar[u.dmn].update(cks_dict)

        if u.pcnfg['params']['enabled']:
            for action_name, action in u.pcnfg['actions'].items():
                u.actions.append([action_name,[]])
                a = action
                for do in a:
                    res = self.do_action(do,u)
                    u.actions[-1][1].append([do,res])
                    print("    ",res," ",do)
        return r


    def do_action(self,do,u): 
        retu = None
        res = None
        arg_ar = None
        no_soup = False
        for arg in do:
            if arg[:2] == 'e_':
                arg_ar = u.pcnfg['elements'][arg]
                if not no_soup:
                    soup = BeautifulSoup(self.d.page_source,'html.parser')
                    ee_retu, res = self.eval_element(arg_ar,soup)
            if arg[0] == '_':
                if arg[:6] == '_click':
                    if not no_soup:
                        selector = self.get_element_path(retu)
                    else:
                        selector = arg_ar[1]
                    wait_time = arg[7:-1]
                    if wait_time:
                        time.sleep(int(wait_time))
                    self.d.click(selector, by="css selector")
                if arg == '_exists':
                    retu = res
                if arg[:5] == '_wait':
                    wait_time = arg[6:-1]
                    if wait_time:
                        time.sleep(int(wait_time))
                if arg == '_no_soup':
                    no_soup=True
                if arg[:7] == '_skipif':
                    act = -1
                    nop=True
                    ele = arg[8:-1]
                    if ele[0] == '!':
                        ele=ele[1:]
                        nop=False
                    if ',' in ele:
                        act, ele = ele.split(',')
                    cond = u.actions[int(act)][1][int(ele)][1]
                    if not ( nop ^ cond ):
                        retu='skipped!'
                        return retu
        return retu


    def eval_element( self, arg_ar, given_soup):
        retu = None
        res = False
        tag = None
        where = False
        tgt = None
        query = {}
        opts  = { '_css':    {'enabled':False, 'val':None, 'used':False}, }
        for item in arg_ar:
            if isinstance(item,list):
                tgt = item
            elif opts['_css']['enabled']:
                where=True
                tag=item
                opts['_css']['val'] = tag
                opts['_css']['enabled'] = False
            elif '=' in item:
                key, value = item.split('=',1)
                if key[0] == '_':
                    tgt = value
                else:
                    query.update({key: value})
            elif item == '_css':
                opts[item]['enabled'], opts[item]['used']=True,True
            elif not where:
                tag = item
                where = True
            else:
                tgt = item
        # ----- get soup
        soup_batch = None
        # - CSS
        if opts['_css']['used']:
            selector = opts['_css']['val']
            soup_batch = given_soup.select(selector)
            if not len(soup_batch):
                return retu, res
        # - QUERY
        else:
            soup_batch = given_soup.find_all(tag, attrs=query) 
        if not len(soup_batch):
            print('                ...bad soup_batch: no len',arg_ar)
            return retu, res

        # ----- get tgt
        soup = soup_batch[0]
        if tgt is None:
            retu = soup
            res = True
        else:
            if tgt:
                child_retu, child_res = self.eval_element(tgt,soup)
                if not child_res:
                    print('                ...bad child_batch',tgt)
                    return retu, res
                retu = child_retu
                res = child_res
        return retu, res      


    def get_element_path(self, element):
        path = []
        while element.parent:
            parent = element.parent
            siblings = parent.find_all(element.name, recursive=False)
            index = siblings.index(element) + 1 if siblings else 1
            path.insert(0, f'{element.name}:nth-of-type({index})')
            element = parent
        return ' > '.join(path)


    def s_fs(self,url,post=False):
        r = None
        cmd     = "request.post" if post else "request.get"
        headers = {"Content-Type": "application/json"}
        fs_data = { 
                    "cmd": cmd, 
                    "url": url,
                    "waitInSeconds": 20,
                    "maxTimeout": 60000,
                    }
        try:
            r = self.s.post(self.s_url, headers=headers, json=fs_data)
        except Exception as err:
            exc_type, value, traceback = sys.exc_info()
            name = exc_type.__name__
            print(f"Other error occurred: {err}")
        return r

        
        
        #download controller
        #checker