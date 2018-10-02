# writing-robot
A twitter-bot that cares deeply about writers. If you're a writer, it cares about you most of all.

## Rationale
A whole bunch of different hashtags have their own dedicated Twitter bots. I noticed that #100DaysOfWriting didn't have a bot, and I had spare API keys hanging around. Then I increased the scope, because that's not a very active hashtag, so now it watches several more.

## Usage
The bot tweets as ![@writingrobot](https://twitter.com/writingrobot). 

Currently it watches several hashtags - #100DaysOfWriting, #RedditWriters, #amwritingHorror, #amwritingFantasy, #amwritingRomance, #amwritingScifi. It doesn't watch #amwriting itself, because that one is so popular that the bot would run afoul of Twitter's rate limits if it tried to keep up, and also the hashtag is full of spam. 

If you tweet with one of those hashtags, it should retweet you, although you might fall through the gaps if you pick a very busy time. If you follow the account, it will eventually follow you back. 

It should tweet once every forty seconds, and update who it follows every 12 hours.

## Dependencies
Tweepy

## Issues & Suggestions
If something goes horribly wrong, please let me know. The bot has a limited ability to call for help if something goes wrong. If that fails and you notice, or if you have any suggestions for improvement, email me at peritract@hotmail.co.uk.
