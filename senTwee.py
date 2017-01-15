import re
import tweepy
from textblob import TextBlob


class MyTwitter:

    def __init__(self):
        self.consumer_key = '<>'
        self.consumer_secret = '<>'

        self.access_token = '<>'
        self.access_token_secret = '<>'

        try:
            self.API = self.authorize()
        except:
            print("App failed: Authentication failed")

    def authorize(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        api = tweepy.API(auth)
        return api

    def clean_tweet(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def sentiment_type(self, tweet):
        cleaned_tweet = self.clean_tweet(tweet)
        blob = TextBlob(cleaned_tweet)

        if blob.sentiment.polarity < 0:
            return 'Negative Sentiment'
        elif blob.sentiment.polarity > 0:
            return 'Positive Sentiment'
        else:
            return 'Neutral Sentiment'

    def get_tweets(self, topic):
        tweets = []

        received_tweets = self.API.search(q=topic, count=4)

        for tweet in received_tweets:
            the_tweet = dict()
            the_tweet['user'] = tweet.user.screen_name
            the_tweet['text'] = tweet.text
            the_tweet['sentiment'] = self.sentiment_type(tweet.text)

            tweets.append(the_tweet)

        return tweets

    def print_tweets(self, topic):
        tweets = self.get_tweets(topic)
        for tweet in tweets:
            st = "User: <{0}> with Sentiment: <{1}> says \n \t {2}".format(
                tweet['user'], tweet['sentiment'], tweet['text'])
            print(st)


def main():
    query = input("Search: ")
    t = MyTwitter()
    t.print_tweets(query)


if __name__ == '__main__':
    main()



