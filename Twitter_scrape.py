# -*- coding: utf-8 -*-
import os
import tweepy
import urllib3
import urllib.request
import urllib.error
import urllib.parse
import sys
from time import sleep

IMAGES_DIR = "OUTPUT_DIR" 
#= Twitter API Key の設定
CONSUMER_KEY        = os.environ.get('TWITTER_API_KEY')
CONSUMER_SECRET     = os.environ.get('TWITTER_API_SECRET_KEY')
ACCESS_TOKEN_SECRET    = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')
ACCESS_TOKEN_KEY = os.environ.get('TWITTER_ACCESS_TOKEN') 

#= 検索キーワード
KEYWORDS = ["ねこ"]

#= 検索オプション
RETURN_PAR_PAGE = 100
NUMBER_OF_PAGES = 10

class ChinoImageDownloader(object):
    def __init__(self):
        super(ChinoImageDownloader, self).__init__()
        self.set_twitter_api()
        self.media_url_list = []

    def run(self):
        for keyword in KEYWORDS:
            self.max_id = None
            for page in range(NUMBER_OF_PAGES):
                self.download_url_list = []
                self.search(keyword, RETURN_PAR_PAGE)
                for url in self.download_url_list:
                    print(url)
                    self.download(url)

    def set_twitter_api(self):
        try:
            auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
            self.api = tweepy.API(auth)
        except Exception as e:
            print("[-] Error: ", e)
            self.api = None

    def search(self, term, rpp):
        try:
            if self.max_id:
                search_result = self.api.search(q=term, rpp=rpp, max_id=self.max_id)
            else:
                search_result = self.api.search(q=term, rpp=rpp)
            for result in search_result:

                #if result.entities.has_key('media'):
                if 'media' in result.entities:
                    for media in result.entities['media']:
                        url = media['media_url_https']
                        if url not in self.media_url_list:
                            self.media_url_list.append(url)
                            self.download_url_list.append(url)
            self.max_id = result.id
        except Exception as e:
            print("[-] Error: ", e)

    def download(self, url):
        print(url)
        url_orig = '%s:orig' % url
        filename = url.split('/')[-1]
        basename = os.path.basename(url)
        savepath = os.path.join(IMAGES_DIR, basename)
        print("saveed in ",savepath)
        try:
            response = urllib.request.urlopen(url_orig)
            #response = urllib2.urlopen(url_orig)
            with open(savepath, "wb") as f:
                #f.write(response.read())
                f.write(response.read())
                sleep(1)
        except Exception as e:
            print("[-] Error: ", e)

def main():
    try:
        downloader = ChinoImageDownloader()
        downloader.run()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
