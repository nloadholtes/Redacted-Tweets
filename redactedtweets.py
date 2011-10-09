#! /usr/bin/env python
#
# redactedtweets.py
# Nick Loadholtes <nick@ironboundsoftware.com>
# Sept 26, 2011
#

import tweepy
import ConfigParser

REDACTED_CHAR = u'\u2588'
ACTION_WORDS = ('to', 'with',)

TEST_TWEET = "I went to work with gusto."

TIMELINE = "http://api.twitter.com/1/statuses/home_timeline.json"
POSTURL = "http://api.twitter.com/1/statuses/update.json"

api = None
config = None

def getTweets(api):
    return  [(x.user.name, '@' +str(x.user.screen_name), x.text) for x in api.home_timeline()]

def postTweet(tweettext):
    status = "status="+tweettext
    pass

def scanTweets(tweets):
    output = []
    for tweet in tweets:
        tmp = redactTweet(tweet[2])
        if tmp is not None:
            print "WAS: ", tweet[2]
            print "NOW: ", tmp
            output.append((tweet[1] ,tmp))
    return output

def redactTweet(tweet):
    words = tweet.split(' ')
    output = unicode("", errors='ignore')
    redact = None
    for word in words:
        if word in ACTION_WORDS:
            redact = word
        if redact and redact != word:
            tmp = [REDACTED_CHAR for x in word] #length of word, substitute redacted_char
            output += "".join(tmp) 
            redact = None
        else:
            output += word
        output += " "
    output = output.strip()
    if output == tweet.strip():
        return None
    return output

def test():
    result = scanTweets([TEST_TWEET])
    print "->" + TEST_TWEET
    print "".join(result)
    assert(result != TEST_TWEET)
    
def main():
    config = ConfigParser.RawConfigParser()
    config.read('config.cfg')
    auth = tweepy.OAuthHandler(config.get('twitter', 'CONSUMER_KEY'),
                      config.get('twitter', 'CONSUMER_SECRET'))
    auth.set_access_token(config.get('twitter', 'ACCESS_TOKEN_KEY'),
                      config.get('twitter', 'ACCESS_TOKEN_SECRET'))
    api = tweepy.API(auth)
#    print api.me().name
    tweets = getTweets(api)
    scanTweets(tweets)

if __name__ == "__main__":
    #test()
    main()
