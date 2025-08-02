import sys


class Fetcher():
    def __init__(self):
        pass

    def start_session(self):

        # session (s)
        import requests
        self.s            = requests.session()

        # flare_solver (fs)
        self.s_fs_timeout = 6000
        r=self.s.post(
            "http://localhost:8191/v1",
            headers={"Content-Type": "application/json"},
            json={ "cmd": "sessions.create"})
        import json
        content = json.loads(r.content)
        status  = content["status"]
        r = None
        try:
            r = self.s.post(
                'https://www.google.com',
                headers={"Content-Type": "application/json"},
                json = { "cmd": "request.get", "url": url, "waitInSeconds": 20, "maxTimeout": 60000, })
        except Exception as err:
            exc_type, value, traceback = sys.exc_info()
            name = exc_type.__name__
            print(f"Error occurred: {err}")
        resp  = json.loads(r.content)
        user_agent       = resp["solution"]["userAgent"]

        # driver (d)
        from seleniumbase import Driver
        self.d = Driver(
            agent=user_agent,
            browser="chrome",
            do_not_track=True,
            headless=True,
            no_sandbox=True,
            uc=True,
            undetectable=True,)
        self.d.set_page_load_timeout(20)


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
            print(status)



if __name__ == "__main__":
    ov = Fetcher()

