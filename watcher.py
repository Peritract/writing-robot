import tweepy
import datetime

class Watcher(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.queue = []
        self.last = datetime.datetime.now()
        self.maintenance = datetime.datetime.now()
        self.functioning = True;
        self.delay = 40

    def essential_maintenance(self):
        #follow all followers
        new_follows = 0
        for follower in tweepy.Cursor(self.api.followers).items():
            if not follower.following and new_follows < 100:
                follower.follow()
                new_follows += 1
        self.maintenance = datetime.datetime.now()

    def handle_queue(self):
        #If there's something in the queue and the last action was long enough ago, act.
        if len(self.queue) > 0 and self.check_time():
            if len(self.queue) > 35:
                self.queue = self.queue[-35:]
            tweet = self.queue.pop(0)
            try:
                tweet.retweet()
            except tweepy.TweepError as e:
                pass
            self.last = datetime.datetime.now()

    def check_time(self):
        #Checks if the last action was long enough ago.
        if datetime.datetime.now() > self.maintenance + datetime.timedelta(hours=12):
            self.essential_maintenance()
        if datetime.datetime.now() > self.last + datetime.timedelta(seconds=self.delay):
            return True
        else:
            return False
    
    def on_status(self, status):
        #Add the tweet to the queue
        if status.in_reply_to_status_id == None and status.retweet_count == 0 and len(status.entities.get('hashtags')) < 5:
            self.queue.append(status)
        
    def on_error(self, error):
        #If something goes wrong, stop streaming, call for help
        self.functioning = False
        self.api.update_status("Help me I am broken. @peritract @dmntdbttrfly")
        return False #disconnect
