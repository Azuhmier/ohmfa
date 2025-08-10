### MASTER
import os
import csv
import sys
import json
import time
import yaml
import pprint
import shutil
import re

from bs4 import BeautifulSoup
import requests
from seleniumbase import Driver
from ohmfa.config_parser import process_item

class Fetcher():

    s = None
    s_url = None
    s_fs_timeout = None
    def __init__(self, dcnfg, archive_path=None):
        self.durls = {}
        self.pwds = {}
        self.fs_domains = []
        self.cookie_jar = {}
        self.d_page_wait = 20
        self.dspt = dcnfg
        self.archive_path = archive_path
        #self.dl_path = "/home/azuhmier/progs/ohmfa/dl"  # Specify your desired path
        self.dl_path = "/home/azuhmier/progs/ohmfa/downloaded_files"  # Specify your desired path


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
        print('dafda')
        self.d = Driver(
            agent=user_agent,
            browser="chrome",
            #devtools=True,
            #log_cdp_events=True,
            do_not_track=True,
            headless=True,
            no_sandbox=True,
            uc=True,
            #external_pdf=True,
            uc_cdp_events=True,
            undetectable=True,
            #uc_subprocess=True,
            #version_main = 130,
            )
        self.d.delete_all_cookies()
        self.d.set_page_load_timeout(self.d_page_wait)
        #self.d.execute_cdp_cmd("Page.setDownloadBehavior", {"behavior": "allow", "downloadPath": self.dl_path})

    def fetch_all(self, start=0, max=0):
        self.cleanup()

        for cnt, durl in enumerate(self.durls):

            if durl.sld != 'archiveofourown':
                max = max + 1
                continue
            if durl.node_type != 'work':
                max = max + 1
                continue

            u = durl.url.geturl()
            print(f"{cnt}: {u}")

            #u directory
            u_fname = u.replace("/","_")
            u_dir = os.path.join(self.archive_path,u_fname)
            os.makedirs(u_dir, exist_ok=True)
            f_fname = str(int(time.time()))
            #f directory
            f_dir = os.path.join(u_dir,f_fname)
            f_dl_dir = os.path.join(f_dir,"dl")
            #f_dl directory
            os.makedirs(f_dl_dir, exist_ok=True)
            f_html_path = os.path.join(f_dir,f_fname+".html")
            f_meta_path = os.path.join(f_dir,f_fname+".info")
            f_log_path = os.path.join(f_dir,f_fname+".log")

            r = self.fetch(durl)

            #fetch file
            with open(f_html_path, 'w') as file:
                file.write(self.d.page_source)
            #fetch info
            with open(f_meta_path, 'w') as file:
                file.write(self.d.page_source)
            logs = {}
            logs["browser"] = self.d.get_log('browser')
            with open(f_log_path, 'w') as file:
                json.dump(logs,file,indent=4)
            
            for filename in os.listdir(self.dl_path):
                file_path = os.path.join(self.dl_path, filename)
                source_file = self.dl_path
                destination_directory = os.path.join(f_dl_dir,filename)

                try:
                    shutil.copy2(file_path, destination_directory)
                    os.remove(file_path)
                    print(f"File '{source_file}' copied to '{destination_directory}' with metadata successfully.")
                except FileNotFoundError:
                    print(f"Error: Source file '{source_file}' not found.")
                except Exception as e:
                    print(f"An error occurred: {e}")
            


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
            print('a')
            time.sleep(2)
            #---------------------------
            self.d.execute_cdp_cmd('Network.enable',{})
            #---------------------------
            for fs_cookie in fs_cookies:
                fs_cookie.update({'domain': u.dmn})
                res = self.d.execute_cdp_cmd('Network.setCookie', fs_cookie)
                #---------------------------
                self.d.execute_cdp_cmd('Network.disable', {})
                #---------------------------
            #---------------------------
            self.d.execute_cdp_cmd('Network.disable', {})
            #---------------------------
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
        print('b')
        time.sleep(2)
        self.d.get(u.url.geturl())
        print('c')
        time.sleep(5)
        cookies = self.d.get_cookies()
        print('d')
        time.sleep(2)
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
            print(u.ws)
        return r


    def do_action(self,do,u): 
        retu = None
        res = None
        arg_ar = None
        no_soup = False
        start_time = 0
        till = start_time
        ii=0
        odo = do
        while ii < len(do):
            arg = do[ii]
            nmstr, item_type, args = process_item(arg,parse_only=True)
            if arg[:2] == 'e_':
                ee_retu = None
                pproc = args[0]
                arg_ar = u.pcnfg['elements'][nmstr]
                
                    
                if not no_soup:
                    soup = BeautifulSoup(self.d.page_source,'html.parser')
                    ee_retu, res = self.eval_element(arg_ar,soup)
            
                if pproc and res:
                    for proc in pproc:
                        if proc == 'text':
                            ee_retu = ee_retu.get_text()
                        else:
                            ee_retu = ee_retu[proc]
                        
                    

                        
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
                if arg == '_!exists':
                    retu = not res
                if arg[:5] == '_wait':
                    wait_time = arg[6:-1]
                    if wait_time:
                        time.sleep(int(wait_time))
                if arg == '_no_soup':
                    no_soup=True
                if nmstr == 'split':
                    for i in args:
                        delim = i[0]
                        idx = int(i[1])
                        ee_retu = ee_retu.split(delim)
                        ee_retu = ee_retu[idx]
                if nmstr =='db':
                    db_name = args[0][0]
                    db_path = args[0][1]
                    if db_name == 'u':
                        u.ws[db_path] = ee_retu
                if nmstr == 'file':
                    fpath = args[0][0]
                    if fpath == 'dl':
                        res = os.path.exists('/home/azuhmier/progs/ohmfa/dl/'+u.ws['title'])
                if nmstr == 'till':
                    if not res:
                        if start_time == 0:
                            max_wait_time = int(args[0][0])
                            start_time = time.time()  # Record the starting time
                            end_time = start_time + max_wait_time  # Calculate the target end time (10 seconds from start)
                        if time.time() < end_time:
                            do = do + odo
                            print(f"    ...waiting: {end_time - time.time()}")
                            time.sleep(5)
                            print(len(do))
                            retu = None
                            res = None
                            arg_ar = None
                            no_soup = False


                if nmstr == 'regex':
                    rgx = None
                    r_pat_name = arg[7:-1]
                    if not 'compiled_regex' in u.pcnfg.keys():
                        u.pcnfg['compiled_regex'] = {}
                    if r_pat_name in u.pcnfg['compiled_regex'].keys():
                        rgx = u.pcnfg['compiled_regex'][r_pat_name]
                    else:
                        r_pat = u.pcnfg['regex'][r_pat_name]
                        rgx = re.compile(r_pat)
                        u.pcnfg['compiled_regex'][r_pat_name] = rgx
                    res = bool(rgx.match(ee_retu))
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
                        break
                        return retu
            ii=ii+1
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

        
    def delete_all_sessions(self):
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


    def cleanup(self):
        """
        Removes all files within a specified directory,
        leaving subdirectories and the directory itself intact.
        """

        # clean download folder
        for filename in os.listdir(self.dl_path):
            file_path = os.path.join(self.dl_path, filename)
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                    #print(f"Removed: {file_path}")
                except OSError as e:
                    print(f"Error removing {file_path}: {e}")

        directory_to_delete = "/home/azuhmier/progs/ohmfa/downloaded_files"  # Replace with the actual path

        if os.path.exists(directory_to_delete) and os.path.isdir(directory_to_delete):
            try:
                shutil.rmtree(directory_to_delete)
                #print(f"Directory '{directory_to_delete}' and its contents have been deleted.")
            except OSError as e:
                print(f"Error deleting directory '{directory_to_delete}': {e}")
        else:
            print(f"Directory '{directory_to_delete}' does not exist or is not a directory.")
        
        # Define the path to the directory you want to clear
        target_directory = "/home/azuhmier/hmofa/archive" 

        # Iterate through all items (files and directories) in the target directory
        for item in os.listdir(target_directory):
            item_path = os.path.join(target_directory, item)

            # Check if the item is a directory
            if os.path.isdir(item_path):
                try:
                    # Recursively remove the subdirectory and its contents
                    shutil.rmtree(item_path)
                    #print(f"Removed subdirectory: {item_path}")
                except OSError as e:
                    print(f"Error removing {item_path}: {e}")

                
        #download controller
        #checker