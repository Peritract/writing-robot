import tweepy
import os
from watcher import Watcher

A_SECRET = "UI1MnbMnQMjmAa6no1FzygEXZ0rFofNaPod7RSU9SeHuv" #os.environ['A_SECRET']
A_TOKEN = "1037748405521539072-Nq1gcU514gbdYt2Hqq75VyLkLi4wlp" #os.environ['A_TOKEN']
C_KEY = "cdhd3UzzURs0oPP0wiFoLFzbo" #os.environ['C_KEY']
C_SECRET = "mN59Ly7nvOqVWkQeFduwOsm5FOdWM71X9fVPEIXWuk0jvI3g8t" #os.environ['C_SECRET']

auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
auth.set_access_token(A_TOKEN, A_SECRET)

API = tweepy.API(auth)

if __name__ == "__main__":

    watcher = Watcher(API) #Instantiate the Tweet handler

    stream = tweepy.Stream(auth=API.auth, listener=watcher) #Start watching the stream
    #Set the filters and run asynchronously
    stream.filter(track=["#redditwriters","#100daysofwriting","#amwritinghorror","#amwritingromance","#amwritingfantasy","#amwritingscifi"], async=True)

    #While the stream is watched by another thread, continually check if the queue needs handling
    while watcher.functioning:
        watcher.handle_queue()

