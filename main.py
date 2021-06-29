from settings import api_key, api_key_secret, access_token, access_token_secret
import tweepy
import textblob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

topic = "Cardano"

since = "2021-06-21"
until = "2021-06-28"

search = f"#{topic} -filter:retweets"

tweet_cursor = tweepy.Cursor(api.search, q=search, language='en', since=since, until= until, tweet_mode="extended").items(500)

tweets = [tweet.full_text for tweet in tweet_cursor]

tweets_df = pd.DataFrame(tweets, columns=["Tweets"])

for _, row in tweets_df.iterrows():
    row["Tweets"] = re.sub("http\S+", "", row["Tweets"])
    row["Tweets"] = re.sub("#\S+", "", row["Tweets"])
    row["Tweets"] = re.sub("@\S+", "", row["Tweets"])
    row["Tweets"] = re.sub("\\n", "", row["Tweets"])

tweets_df["Polarity"] = tweets_df["Tweets"].map(lambda tweet: textblob.TextBlob(tweet).sentiment.polarity)
tweets_df["Sentiment"] = tweets_df["Polarity"].map(lambda pol: '+' if pol > 0 else '-')

positive = tweets_df[tweets_df.Sentiment == "+"].count()["Tweets"]
negative = tweets_df[tweets_df.Sentiment == "-"].count()["Tweets"]

plt.bar([0, -1], [positive, negative], label=["Positive", "Negative"], color=["green", "red"])
plt.legend()

plt.show()