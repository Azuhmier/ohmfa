import requests
from bs4 import BeautifulSoup
class Fetcher():
    def __init__(self):
        header = {
            'User-Agent':[],
            'Referer':[],
            'Host':[],      
            'origin':[],
            'Content-Length':[98,102],
            'DNT':[1],
            'Upgrade-Insecure-Requests':[1],
            'Accept-Encoding':[
                'gzip',
                'deflate',
                'br',
                'zstd'],
            'Accept-Language':[
                'en-US',
                'en',
                {
                    'q': [
                        0.5]}],
            'Accept':[
                '*/*',
                'text/html',
                'application/xhtml+xml'
                'application/xml',
                'image/avif',
                'image/webp',
                'image/png'
                'image/svg+xml',
                {
                    'q': [
                        0.8,0.9]}],
            'Connection':[
                'keep-alive' ],
            'Content-Type':[
                'application/x-www-form-urlencoded',
                {
                    'charset':[
                        'UTF-8']}],
            'Priority':[
                'u=4',
                'u=0',
                'i'],
            'Sec-Fetch-Site':[
                'cross-site',
                'none',
                'same-origin' ],
            'Sec-Fetch-Dest':[
                'document',
                'empty',
                'iframe' ],
            'Sec-Fetch-Mode':[
                'navigate'],
            'Sec-Fetch-User':[
                '?1' ],
            'X-Requested-With':[
                'XMLHttpRequest'],
        }
