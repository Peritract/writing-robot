import tweepy
import datetime

class Watcher(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.queue = []
        self.last = datetime.datetime.now()
        self.maintenance = datetime.datetime.now()
        self.seasonal = datetime.datetime.now()
        self.functioning = True;
        self.delay = 40
        self.events = {
            "23/1": "Today is my creator's birthday. Happy Birthday, @Peritract.",
            "15/10": "@DmntdBttrfly If this works then seasonal tweets will work.",
            "20/10": "Super excited for #NaNoWriMo. Can't wait to see what everyone is working on.",
            "31/10": "#NaNoWriMo starts tomorrow! Are you ready?",
            "1/11": "Today is day 1 of #NaNoWriMo. Good luck to everyone taking part!",
            "2/11": "Day 2 of #NaNoWriMo. What's your story about?",
            "3/11": "Day 3 of #NaNoWriMo. Tell me about your main character.",
            "4/11": "Day 4 of #NaNoWriMo. How do you plan?",
            "5/11": "Day 5 of #NaNoWriMo. Describe your plot in one sentence.",
            "6/11": "Day 6 of #NaNoWriMo. Share your first lines with me!",
            "7/11": "Day 7 of #NaNoWriMo. What's your writing top tip?",
            "8/11": "Day 8 of #NaNoWriMo. How is it going so far?",
            "9/11": "Day 9 of #NaNoWriMo. What genre is your story?",
            "10/11": "1/3 of the way through #NaNoWriMo. Keep going!",
            "11/11": "Day 11 of #NaNoWriMo. What's your word count?",
            "12/11": "Day 12 of #NaNoWriMo. Describe your story in 3 words.",
            "13/11": "Day 13 of #NaNoWriMo. How do you deal with writers' block?",
            "14/11": "Day 14 of #NaNoWriMo. Tell me about your villain.",
            "15/11": "Half-way through #NaNoWriMo! Are you still on schedule?",
            "16/11": "Day 16 of #NaNoWriMo. What's the best sentence you've written so far?",
            "17/11": "Day 17 of #NaNoWriMo. What are the themes of your story?",
            "18/11": "Day 18 of #NaNoWriMo. Do you let anyone read your story before it's finished?",
            "19/11": "Day 19 of #NaNoWriMo. If your story was turned into a film, who would you want as actors?",
            "20/11": "2/3 of the way through #NaNoWriMo. You can do it!",
            "21/11": "Day 21 of #NaNoWriMo. Where do you write?",
            "22/11": "Day 22 of #NaNoWriMo. How much did you write on your most productive day?",
            "23/11": "Day 23 of #NaNoWriMo. What three adjectives best describe your story?",
            "24/11": "Day 24 of #NaNoWriMo. What's your favourite scene?",
            "25/11": "Day 25 of #NaNoWriMo. How is it going?",
            "26/11": "Day 26 of #NaNoWriMo. What's the worst plot hole you've accidentally created?",
            "27/11": "Day 27 of #NaNoWriMo. What's your word count?",
            "28/11": "Day 28 of #NaNoWriMo. What author is your idol?",
            "29/11": "Day 29 of #NaNoWriMo. Nearly There!",
            "30/11": "Last day of #NaNoWriMo! How much have you got left to write?",
            "1/12": "#NaNoWriMo is finished for another year. Well done to everyone who tried, and congraluations to everyone who succeeded!",
            "25/12": "Merry Christmas."
            }

    def essential_maintenance(self):
        #follow all followers
        new_follows = 0
        for follower in tweepy.Cursor(self.api.followers).items():
            if not follower.following and new_follows < 100:
                follower.follow()
                new_follows += 1
        self.maintenance = datetime.datetime.now()

    def seasonal_actions(self):
        today = datetime.datetime.now()
        today = "{0}/{1}".format(today.day, today.month)
        if today in self.events:
            try:
                self.api.update_status(self.events[today])
            except:
                pass
        self.seasonal = datetime.datetime.now()

    def check_events(self):
        current = datetime.datetime.now()
        if current > self.maintenance + datetime.timedelta(hours=12):
            self.essential_maintenance()
        elif current > self.seasonal + datetime.timedelta(hours=24):
            self.seasonal_actions()


    def check_time(self):
        #Checks if the last action was long enough ago.
        if datetime.datetime.now() > self.last + datetime.timedelta(seconds=self.delay):
            return True
        else:
            return False

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
        self.check_events()
    
    def on_status(self, status):
        #Add the tweet to the queue
        if status.in_reply_to_status_id == None and status.retweet_count == 0 and len(status.entities.get('hashtags')) < 5 and status.user.screen_name != "WritingRobot" and not status.text.startswith("RT @") and not hasattr(status, 'retweeted_status'):
            self.queue.append(status)
        
    def on_error(self, error):
        #If something goes wrong, stop streaming, call for help
        self.functioning = False
        self.api.update_status("Help me I am broken. @peritract @dmntdbttrfly")
        return False #disconnect
