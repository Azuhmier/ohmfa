import sys
import copy

def gen_from_abr(abr):
    abrvs = {
        'a03':  'archiveofourown',
        'sf':   'sofurry',
        'ff':   'fanfiction',
        'fl':   'fiction',
        'faf':  'furaffinity',
        'ltca': 'literotica',
        'mcst': 'mcstories',

        'pstb': 'pastebin',
        'rt':   'rentry',
        'gstb': 'ghostbin',
        'hrdb': 'hardbin',
        'ponb': 'poneb',
        'psta': 'psstaudio',
        'pef':  'pastefs',

        'bf':   'blokfort',
        'sg':   'snekguy',

        'cbx':  'catbox',
        'gg':   'google',
        'mg':   'mega',

        'gt':   'git',
        'gtuc': 'githubusercontent',

        'itch': 'itch',
        'sntg':  'snootgame',

        'rdt':  'reddit',
    }
    retu = abr
    if abr in abrvs:
        retu = abrvs[abr]
    return retu

    