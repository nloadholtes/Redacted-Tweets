#! /usr/bin/env python
#
# redactedtweets.py
# Nick Loadholtes <nick@ironboundsoftware.com>
# Sept 26, 2011
#

import tweepy
import ConfigParser
import codecs

REDACTED_CHAR = u'\u2588'
ACTION_WORDS = ('to', 'with', 'in', 'the',)

TEST_TWEET = "I went to work with gusto."

api = None
config = None

def getTweets(api):
    return  [(x.user.name, '@' +str(x.user.screen_name), x.text) for x in api.home_timeline()]

def postTweet(api, tweettext):
    pass

def scanTweets(tweets, action_words, redacted_char):
    output = []
    for tweet in tweets:
        if tweet[2].find('RT @') != -1:
            continue
        tmp, count = redactTweet(tweet[2], action_words, redacted_char)
        if tmp is not None and count > 1:
            output.append((tweet[1] ,tmp))
    return output

def redactTweet(tweet, action_words, redacted_char):
    words = tweet.split(' ')
    output = unicode("", errors='ignore')
    redact = None
    count = 0
    for word in words:
        if word in action_words:
            redact = word
        if redact and redact != word and len(word) > 1:
            tmp = [redacted_char for x in word] #length of word, substitute redacted_char
            output += u''.join(tmp)
            redact = None
            count += 1
        else:
            output += word
        output += " "
    output = output.strip()
    if output == tweet.strip():
        return None, count
    return output, count

def test():
    result = scanTweets([TEST_TWEET])
    print "->" + TEST_TWEET
    print "".join(result)
    assert(result != TEST_TWEET)

def main(configfilename='config.cfg'):
    config = ConfigParser.RawConfigParser()
    config.readfp(codecs.open(configfilename, "r", "utf8"))
    auth = tweepy.OAuthHandler(config.get('twitter', 'CONSUMER_KEY'),
                      config.get('twitter', 'CONSUMER_SECRET'))
    auth.set_access_token(config.get('twitter', 'ACCESS_TOKEN_KEY'),
                      config.get('twitter', 'ACCESS_TOKEN_SECRET'))
    actionwords = config.get('twitter', 'ACTION_WORDS')
    redactedchar = config.get('twitter', 'REDACTED_CHAR')
    if actionwords is None:
        actionwords = ACTION_WORDS
    if redactedchar is None:
        redactedchar = REDACTED_CHAR
    api = tweepy.API(auth)
    tweets = getTweets(api)
    for x in scanTweets(tweets, actionwords, redactedchar):
        txt = "RT " + x[0] + ": " + x[1]
        api.update_status(txt[:140])

if __name__ == "__main__":
    #test()
    main()
