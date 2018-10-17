import tweepy
import os
from writing_watcher import Watcher

A_SECRET = os.environ['A_SECRET']
A_TOKEN = os.environ['A_TOKEN']
C_KEY = os.environ['C_KEY']
C_SECRET = os.environ['C_SECRET']

auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
auth.set_access_token(A_TOKEN, A_SECRET)

API = tweepy.API(auth)

if __name__ == "__main__":

    watcher = Watcher(API) #Instantiate the Tweet handler

    stream = tweepy.Stream(auth=API.auth, listener=watcher, tweet_mode='extended') #Start watching the stream
    #Set the filters and run asynchronously
    stream.filter(track=watcher.filter, async=True)

    #While the stream is watched by another thread, continually check if the queue needs handling
    while watcher.running:
        watcher.handle_queue()

