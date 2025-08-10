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
d.get('https://archiveofourown.org/works/68440986')
time.sleep(6000)
d.quit()