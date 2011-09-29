#! /usr/bin/env python
#
# redactedtweets.py
# Nick Loadholtes <nick@ironboundsoftware.com>
# Sept 26, 2011
#

REDACTED_CHAR = u'\u2588'
ACTION_WORDS = ('to', 'with', )

TEST_TWEET = "I went to work with gusto."

PEOPLE_TO_WATCH = ('first', 'second')

def getTweets():
    pass

def scanTweets(tweets):
    output = []
    for tweet in tweets:
        print "->" + tweet
        tmp = redactTweet(tweet)
        if tmp:
            output.append(tmp)
    return output

def redactTweet(tweet):
    words = tweet.split(' ')
    output = ""
    for word in words:
        if word in ACTION_WORDS:
            tmp = [REDACTED_CHAR for x in word]
            output += "".join(tmp)  + " " #length of word, substitute redacted_char
        else:
            output += word + " "
    if output == words:
        return None
    return output

def test():
    print scanTweets([TEST_TWEET])

if __name__ == "__main__":
    test()