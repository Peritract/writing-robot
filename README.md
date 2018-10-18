# writing-robot
A twitter-bot that cares deeply about writers. If you're a writer, it cares about you most of all.

## Rationale
A whole bunch of different hashtags have their own dedicated Twitter bots. I noticed that #100DaysOfWriting didn't have a bot, and I had spare API keys hanging around. Then I increased the scope, because that's not a very active hashtag, so now it watches several more.

## Usage
The bot tweets as [@writingrobot](https://twitter.com/writingrobot). 

Currently it watches several hashtags - #100DaysOfWriting, #1linewed, #amwritingHorror, #amwritingFantasy, #amwritingRomance, #amwritingScifi.It doesn't watch #amwriting, because that hashtag is incredibly prolific, which would mean the others got ignored, and also because the majority of what comes through #amwriting is overly-hashtagged spam. 

If you tweet with one of those hashtags, it should retweet you, although you might fall through the gaps if you pick a very busy time. If you tweet with more than four hashtags, it will ignore you - this is a counter-measure against spam and also those dreadful people who hashtag every second word. 

If you follow the account, it will eventually follow you back. 

It should tweet once every four minutes, and update who it follows every 24 hours. Sometimes, it will post tweets for people to engage with. Please do. 

## Expansion plans

* Not retweeting blocked people (cut down on accidental signal boosting for ads)
* unfollowing non-followers (to stop the ratio getting throttled)
* Only retweeting #1linewed on Wednesdays.
* Weekly tweets - an every Friday roundup or something? 

## Dependencies
Tweepy

## Issues & Suggestions
If something goes horribly wrong, please let me know. The bot has a limited ability to call for help if it encounters a problem. If that fails and you notice, or if you have any suggestions for improvement, email me at peritract@hotmail.co.uk.
