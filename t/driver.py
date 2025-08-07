### MASTER
from seleniumbase import Driver
import time
# --------- driver
d = Driver(
    browser="chrome",
    no_sandbox=True,
    uc=True,
    undetectable=True,
)
downloads_folder = "/home/azuhmier/progs/ohmfa/dl"  # Specify your desired path
d.execute_cdp_cmd("Page.setDownloadBehavior", {"behavior": "allow", "downloadPath": downloads_folder})
d.get('https://archiveofourown.org/works/68440986')
time.sleep(600)
d.quit()