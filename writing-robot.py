import tweepy
import os
import datetime

from time import sleep
from watcher import Watcher

A_SECRET = os.environ['A_SECRET']
A_TOKEN = os.environ['A_TOKEN']
C_KEY = os.environ['C_KEY']
C_SECRET = os.environ['C_SECRET']

auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
auth.set_access_token(A_TOKEN, A_SECRET)

API = tweepy.API(auth)

if __name__ == "__main__":
    queue = []
    watcher = Watcher(API)
    stream = tweepy.Stream(auth=API.auth, listener=watcher)
    stream.filter(track=["#redditwriters","#100daysofwriting"], async=True)
    count = 0
    while watcher.functioning:
        watcher.handle_queue()
        sleep(10)
