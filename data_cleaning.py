import datetime
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import string
from PIL import Image
import re #regular expression
from nltk.corpus import stopwords
def remove_punctuation(text):
    for punctuation in string.punctuation:
        text = text.replace(punctuation, "")
    return text.strip(' ')

#removes URLs
def removes_url(text):
    text = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', '', text)
    return text.strip(' ')

#removes stop-words
def remove_stopwords(text):
    StopWords = stopwords.words("english") + ['tech', 'Want', 'take', 'work', 'way', 'employee', 'Read', 'share', 'Watch', 'de', 'need', 'Want', 'company', 'companies','day', 'experience', 'today', 'Find', 'Check', 'SAPPHIRENOW', 'top', 'Video', 'year', 'Take look', 'learn', 'know', 'video', 'today', 'see', 'join', 'time', 'via', 'need', 'Check', 'know', 'Blog', 'live', 'use', 'Take', 'new', 'best', 'great', 'good', 'one', 'SAP', 'See', 'help', 'business', 'check', 'Video', 'Learn', 'Business', 'technology', 'way', 'make']
    final = ' '.join([word for word in text.split() if word not in StopWords])
    return final.strip(' ')

#removes # and @ in the beginning of each word. ex: #Good -> Good
def remove_hashtag(text):
    new_text = ""
    for words in text.split():
        if words.startswith('@'): #remove @ amd #
            new_text += words[1:]
            new_text += ' '
        else:
            new_text += words
            new_text += ' '
    return new_text.strip(' ')

#removes # and @ even between words. ex: #life#is#good -> life is good
def remove_hash_symbol(text):
    to_be_removed = ['#', '@']
    for prohibited_symbol in to_be_removed:
        text = text.replace(prohibited_symbol, ' ')
    text = ' '.join(text.split())
    return text.strip(' ')

def timeConversion(tweet):
    tweetTimeInt = int(int(float(tweet['created_at']))/1000)
    t = datetime.datetime.fromtimestamp(tweetTimeInt)
    fmt = "%Y-%m-%d %H:%M:%S"
    return t.strftime(fmt)

def generateWordcloud(cleanedTweets):
    # join tweets to a single string
    words = ' '.join(cleanedTweets['text'])

    # remove URLs, RTs, and twitter handles
    no_urls_no_tags = " ".join([word for word in words.split()
                                if 'http' not in word
                                and not word.startswith('@')
                                and word != 'RT'
                                ])
    import numpy as np
    sap_mask = np.array(Image.open("SAP.jpg"))
    stopwords = set(STOPWORDS)
    stopwords.add("SAP")

    wc = WordCloud(font_path = 'CabinSketch-Bold.ttf',
                   background_color="white",
                   max_words=30,
                   width=600, height=300,
                   stopwords=stopwords).generate(no_urls_no_tags)

    plt.figure(figsize=(20, 10), facecolor='k')
    plt.imshow(wc)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()


    plt.imshow(wc)
    #plt.axis('off')
    plt.savefig('my_twitter_wordcloud_1.png', dpi=300)
    plt.show()


if __name__ == '__main__':
    colnames = ['favorites', 'created_at', 'retweets', 'text']

    df = pd.read_csv('sap1.csv', usecols=colnames)
    #df.describe()

    tweet = df
    cleaned_tweets = []
    cleaned_tweets_2009 = []
    cleaned_tweets_2010 = []
    cleaned_tweets_2011 = []
    cleaned_tweets_2012 = []
    cleaned_tweets_2013 = []
    cleaned_tweets_2014 = []
    cleaned_tweets_2015 = []
    cleaned_tweets_2016 = []
    cleaned_tweets_2017 = []
    for index, tw in tweet.iterrows():
        tweetText = tw['text']
        twNourl = removes_url(tweetText)
        twClean = remove_stopwords(twNourl)
        twRmhashtag = remove_hashtag(twClean)
        tweetTime = timeConversion(tw)
        tw['text'] = twRmhashtag
        tw['created_at'] = tweetTime
        year = tw['created_at'][:4]
        cleaned_tweets.append(tw)
        if year == '2009':
            cleaned_tweets_2009.append(tw)
        elif year == '2010':
            cleaned_tweets_2010.append(tw)
        elif year == '2011':
            cleaned_tweets_2011.append(tw)
        elif year == '2012':
            cleaned_tweets_2012.append(tw)
        elif year == '2013':
            cleaned_tweets_2013.append(tw)
        elif year == '2014':
            cleaned_tweets_2014.append(tw)
        elif year == '2015':
            cleaned_tweets_2015.append(tw)
        elif year == '2016':
            cleaned_tweets_2016.append(tw)
        elif year == '2017':
            cleaned_tweets_2017.append(tw)
    cleaned_tweets = pd.DataFrame(cleaned_tweets)
    cleaned_tweets_2009 = pd.DataFrame(cleaned_tweets_2009)
    cleaned_tweets_2010 = pd.DataFrame(cleaned_tweets_2010)
    cleaned_tweets_2011 = pd.DataFrame(cleaned_tweets_2011)
    cleaned_tweets_2012 = pd.DataFrame(cleaned_tweets_2012)
    cleaned_tweets_2013 = pd.DataFrame(cleaned_tweets_2013)
    cleaned_tweets_2014 = pd.DataFrame(cleaned_tweets_2014)
    cleaned_tweets_2015 = pd.DataFrame(cleaned_tweets_2015)
    cleaned_tweets_2016 = pd.DataFrame(cleaned_tweets_2016)
    cleaned_tweets_2017 = pd.DataFrame(cleaned_tweets_2017)
    generateWordcloud(cleaned_tweets)
    generateWordcloud(cleaned_tweets_2009)
    generateWordcloud(cleaned_tweets_2010)
    generateWordcloud(cleaned_tweets_2011)
    generateWordcloud(cleaned_tweets_2012)
    generateWordcloud(cleaned_tweets_2013)
    generateWordcloud(cleaned_tweets_2014)
    generateWordcloud(cleaned_tweets_2015)
    generateWordcloud(cleaned_tweets_2016)
    generateWordcloud(cleaned_tweets_2017)