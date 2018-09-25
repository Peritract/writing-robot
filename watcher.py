import tweepy
import datetime

class Watcher(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.queue = []
        self.last = datetime.datetime.now()
        self.functioning = True;
        self.delay = 40

    def handle_queue(self):
        #If there's something in the queue and the last action was long enough ago, act.
        if len(self.queue) > 0 and self.check_time():
            print("printing!")
            tweet = self.queue.pop(0)
            tweet.retweet()
            self.last = datetime.datetime.now()

    def check_time(self):
        #Checks if the last action was long enough ago.
        if datetime.datetime.now() > self.last + datetime.timedelta(seconds=self.delay):
            return True
        else:
            return False
    
    def on_status(self, status):
        #Add the tweet to the queue
        print("GOT ONE")
        self.queue.append(status)
        
    def on_error(self, error):
        #If something goes wrong, stop streaming, call for help
        self.functioning = False
        self.api.update_status("Help me I am broken. @peritract @dmntdbttrfly")
        return False #disconnect
