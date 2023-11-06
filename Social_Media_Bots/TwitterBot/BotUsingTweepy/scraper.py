import tweepy
import configparser
import pandas as pd
import time

OUTPUT_DIR = "data"

config = configparser.RawConfigParser()
config.read('config.ini')
consumer_key = config.get('dev', 'consumer_key')
consumer_secret = config.get('dev', 'consumer_secret')
access_token = config.get('dev', 'access_token')
access_token_secret = config.get('dev', 'access_token_secret')
bearer_token = config.get('dev', 'bearer_token')

client = tweepy.Client(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret,
    bearer_token=bearer_token,
    wait_on_rate_limit=True
)

def tweet(text):
    response = client.create_tweet(text=text)
    print(response)

def get_tweets_by_query(text_query, count, lang='en', result_type='mixed', filter_rt=True):
    try:
        # Filter retweets
        if filter_rt:
            text_query = text_query + " -filter:retweets"

        tweets = client.search_recent_tweets(query=text_query, user_auth=True)

        tweets_list = [[tweet.created_at, tweet.id, tweet.full_text] for tweet in tweets]

        tweets_df = pd.DataFrame(tweets_list,columns=['Datetime', 'Tweet Id', 'Text'])

        filename = text_query.replace(' ', '_')

        tweets_df.to_csv(f'{OUTPUT_DIR}/{filename}.txt', sep=',', index = False)
    except BaseException as e:
        print('failed to get tweets,',str(e))


tweet("hello world!")

get_tweets_by_query("chatgpt", 10)
