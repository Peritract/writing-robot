import datetime
import tweepy
from random import random
from time import sleep

class Watcher(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api #Twitter auth details
        
        if not self.api.verify_credentials():
            self.on_error("Invalid credentials.")

        self.running = True

        #Keeps track of what day the bot thinks it is.
        #Initially set to the day before, so that it updates on the day the program starts. 
        self.date = "{0}/{1}".format((datetime.datetime.now() - datetime.timedelta(days=1)).day, (datetime.datetime.now() - datetime.timedelta(days=1)).month)
        

        #The hashtags the stream will watch for.
        self.filter = ["#100daysofwriting",
                       "#amwritinghorror",
                       "#amwritingromance",
                       "#amwritingfantasy",
                       "#amwritingscifi",
                       "#1linewed",
                       "#redditwriters",
                       "#nanowrimo"]
        
        self.blocked = self.update_blocks()
        
        self.queue = [] #the tweets to be posted
        self.retweet_delay = 240 #how long between tweets in seconds
        self.last_retweet = datetime.datetime.now() #The last time it tweeted

        #Tweets for specific days of the year
        self.events = {
            "23/1": "Today is my creator's birthday. Happy Birthday, @Peritract.",
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

        if not self.api.verify_credentials():
            self.on_error("Invalid credentials.")

    # Little helper functions

    def handle_cursor_limit(self, cursor):
        # When Twitter Squawks, pause briefly.
        while True:
            try:
                yield cursor.next()
            except tweepy.RateLimitError:
                sleep(15 * 60)

    def get_date(self):
        #Gets today's date in the format D/MM
        today = datetime.datetime.now()
        return "{0}/{1}".format(today.day, today.month)

    def get_queue_chance(self):
        # Returns a sub-1 number - the chance that a tweet will be added to the queue
        if len(self.queue) < 5:
            return 1
        elif len(self.queue) > 5 + 12:
            return 0
        else:
            return ((1 / (1 + len(self.queue) - 5)) * 0.95)

    def check_age(self, time):
        # Returns True if a tweet is less than an hour old. 
        if time > datetime.datetime.now() - datetime.timedelta(hours=1):
            return True
        return False

    def check_last_retweet_time(self):
        # If the last tweet retweeted was more than [self.retweet_delay] seconds ago.
        if datetime.datetime.now() > self.last_retweet + datetime.timedelta(seconds=self.retweet_delay):
            return True
        return False

    def filter_hashtags(self, hashtags):
        # Searches for specific hashtags for days of the week.
        # Returns True if the tweet passes the filter
        weekday = datetime.datetime.today().weekday()
        if weekday == 2:
            #On Wednesdays, only let #1linewed and #100DaysOfWriting through
            for tag in hashtags:
                if tag["text"].lower() == "1linewed" or tag["text"].lower() == "100daysofwriting":
                    return True
            return False
        
        #Barring a more applicable filter, allow everything as default
        return True

    # Central, generally directly involved with Twitter, functions

    def handle_queue(self):
        # Decides whether to tweet or not.
        if len(self.queue) > 0 and self.check_last_retweet_time():
            # If there is anything in the queue, take the oldest one and retweet it.
            tweet = self.queue.pop(0)
            try:
                tweet.retweet()
            except tweepy.TweepError as error:
                self.on_error(error)
            self.last_retweet = datetime.datetime.now() # Reset the delay
        self.prune_queue() # Stop the queue getting stale
        self.daily_actions() # Check for a daily tweet

    def update_followers(self):
        #Loop through all current followers and follow them back. 
        for follower in self.handle_cursor_limit(tweepy.Cursor(self.api.followers).items(200)):
            if not follower.following:
                follower.follow()
                sleep(5)

    def update_blocks(self):
        # Update the list of blocked users
        return self.api.blocks_ids()["ids"]

    def daily_actions(self):
        now = datetime.datetime.now()
        threshold = now.replace(hour=16, minute=0, second=0, microsecond=0)
        if now > threshold: #If it is after 4pm
            today = self.get_date() 
            if self.date != today: #If it hasn't been checked yet today
                self.date = today # Update when last checked
                
                # Post a specific tweet for the day of the year.
                if today in self.events: # If there is an event tweet
                    self.post_tweet(self.events[today])

                # Update follower counts
                self.update_followers()

                # Update the block list 
                self.blocked = self.update_blocks()
        
                
    def consider_tweet(self, status):
        # Determines if a tweet from the stream should be added to the queue.

        #Disqualifying conditions
        if len(status.entities.get('hashtags')) > 4:
            return False
        elif not self.filter_hashtags(status.entities.get('hashtags')):
            return False
        elif status.user.screen_name == "WritingRobot":
            return False
        elif status.text.startswith("RT @"):
            return False
        elif hasattr(status, 'retweeted_status'):
            return False
        elif hasattr(status, 'quoted_status_id'):
            return False
        elif status.in_reply_to_status_id != None:
            return False
        elif status.retweeted == True:
            return False
        elif status.retweet_count != 0:
            return False
        elif status.user.id in self.blocked:
            return False

        #Semi-random chance, partially dependent on length of queue:
        chance = self.get_queue_chance()
        if chance < random():
            return False

        # Actually accept the tweet
        return True

    def prune_queue(self):
        # Removes tweets that are too old from the queue.
        if len(self.queue) > 20:
            n_queue = []
            for i in range(0, len(self.queue)):
                if self.check_age(self.queue[i].created_at):
                    n_queue.append(self.queue[i])
            self.queue = n_queue
        
    def post_tweet(self, status):
        #actually post a tweet
        try:
            self.api.update_status(status)
        except tweepy.TweepError as error:
            self.on_error(error)
    
    def on_status(self, status):
        # Whenever a tweet comes in from the stream
        if self.consider_tweet(status):
            self.queue.append(status)
        
    def on_error(self, error):
        # If twitter sends an error back from the stream
        print(datetime.datetime.now(), "Error:", error.response.text)
        if error.api_code != 144: #Status to be retweeted no longer exists - doesn't need to stop anything
            self.running = False
            self.post_tweet("@peritract Help me I am broken.")
