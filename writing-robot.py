import tweepy
import os
from time import sleep

A_SECRET = os.environ.get('A_SECRET')
A_TOKEN = os.environ.get('A_TOKEN')
C_KEY = os.environ.get('C_KEY')
C_SECRET = os.environ.get('C_SECRET')

auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
auth.set_access_token(A_TOKEN, A_SECRET)

API = tweepy.API(auth)

if __name__ == "__main__":
    while True:
        print("starting")
        #Get the last 50 tweets that match the criteria
        for tweet in tweepy.Cursor(API.search, q='#amwriting OR #redditwriters OR #100daysofwriting', rpp=50).items(50):
            if not tweet.retweeted:
                tweet.retweet()
                sleep(15)
    sleep(60)
