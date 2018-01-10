import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import pandas as pd

#
# def clean_tweet(tweet):
#     '''
#     Utility function to clean tweet text by removing links, special characters
#     using simple regex statements.
#     '''
#     return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])
#                            | (\w +:\ / \ / \S +)", " ", tweet).split())

def get_tweet_sentiment(tweet):
    '''
    Utility function to classify sentiment of passed tweet
    using textblob's sentiment method
    '''
    # create TextBlob object of passed tweet text
    analysis = TextBlob(tweet)
    # set sentiment
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

def analyzeTweets(tweetsReceived):
    '''
    Main function to fetch tweets and parse them.
    '''
    # empty list to store parsed tweets
    tweets = []

    try:
        # call twitter api to fetch tweets
        #fetched_tweets = self.api.search(q=query, count=count)
        fetched_tweets = tweetsReceived
        # parsing tweets one by one
        for tweet in fetched_tweets:
            # empty dictionary to store required params of a tweet
            parsed_tweet = {}

            # saving text of tweet
            parsed_tweet['text'] = tweet['text']
            # saving sentiment of tweet
            parsed_tweet['sentiment'] = get_tweet_sentiment(tweet['text'])

            # appending parsed tweet to tweets list
            if tweet.retweet_count > 0:
                # if tweet has retweets, ensure that it is appended only once
                if parsed_tweet not in tweets:
                    tweets.append(parsed_tweet)
            else:
                tweets.append(parsed_tweet)

        # return parsed tweets
        return tweets

    except tweepy.TweepError as e:
        # print error (if any)
        print("Error : " + str(e))


def main():
    # creating object of TwitterClient Class
    #api = TwitterClient()
    # calling function to get tweets
    colnames = ['favorites', 'created_at', 'retweets', 'text']

    # df = pd.read_csv('sap1.csv', usecols=colnames)
    # df.describe()
    df = pd.read_csv('cleaned_mention_tweets.csv', usecols=colnames)
    tweets = df

    tweets = analyzeTweets(tweets)
    #tweets = api.get_tweets(query='Donald Trump', count=200)

    # picking positive tweets from tweets
    ptweets = [tweet for tweet in finaltweets if tweet['sentiment'] == 'positive']
    # percentage of positive tweets
    print("Positive tweets percentage: {} %".format(100 * len(ptweets) / len(finaltweets)))
    # picking negative tweets from tweets
    ntweets = [tweet for tweet in finaltweets if tweet['sentiment'] == 'negative']
    # percentage of negative tweets
    print("Negative tweets percentage: {} %".format(100 * len(ntweets) / len(finaltweets)))
        # percentage of neutral tweets
    print("Neutral tweets percentage: {} % \
        ".format(100 * len(tweets - ntweets - ptweets) / len(finaltweets)))

    # printing first 5 positive tweets
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])

    # printing first 5 negative tweets
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])


if __name__ == "__main__":
    # calling main function
    main()

    finaltweets = []
    for count in range(0, 20095):
        parsed_tweet = {}
        parsed_tweet['text'] = tweets['text'].values[count]
        parsed_tweet['sentiment'] = get_tweet_sentiment(tweets['text'].values[count])
        if tweets['retweets'].values[count] > 0:
            if parsed_tweet not in finaltweets:
                finaltweets.append(parsed_tweet)
        else:
            finaltweets.append(parsed_tweet)
