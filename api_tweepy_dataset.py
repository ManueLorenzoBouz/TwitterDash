import pandas as pd
import numpy as np
import tweepy
import ast

APIkey = 'YOUR APIKEY'
APIsecretkey = 'YOUR APISECRETKEY'
AT = 'YOUR AT'
ATsecret = 'YOUR SECRET AT'
auth = tweepy.OAuthHandler(APIkey,APIsecretkey)
auth.set_access_token(AT, ATsecret)
api = tweepy.API(auth, 
                       wait_on_rate_limit = True, 
                       wait_on_rate_limit_notify = True)

influencers_tweets = tweepy.Cursor(api.search, q = ['peopleanalytics', 'HR analytics'], tweet_mode = 'extended', 
                              wait_on_rate_limit = True).items(1000)

tweets=list()
for tweet in influencers_tweets:
  id_tweet=tweet.id
  data={
        'tweet_id':tweet.id,
        'date':tweet.created_at.strftime('%Y-%m-%dT%H:%M:%S'),
        'user_sn':tweet.user.screen_name,
        'tweet_text':tweet.full_text,
        'follower_count':tweet.user.followers_count,
        'retweet_count':tweet.retweet_count,
        'user_mentions':tweet.entities['user_mentions']
        }
  tweets.append(data)
  
tweets_df = pd.DataFrame(tweets)

aristas=list()
for iid,row in tweets_df.iterrows():
    if len(row[6]) > 0:
        user_sn=row[2]
        date=row[1]
        for iid_1,item in enumerate(ast.literal_eval(str(row[6]))):
            data={
                'source':user_sn,
                'target':ast.literal_eval(str(row[6]))[iid_1]['screen_name'],
                'date':date
            }
            aristas.append(data)
network_df = pd.DataFrame(aristas)

users_relevance = tweets_df.groupby(by = 'user_sn', as_index = False).agg({'follower_count': 'max', 'retweet_count': 'sum', 'tweet_text':'count'})
users_relevance.rename(
    columns = {'user_sn': 'User name', 'follower_count': 'Followers', 'retweet_count': 'Retweets received', 'tweet_text': 'Nº of Tweets'}
, inplace = True)

users_active_conection = network_df.groupby(by = 'source', as_index = False).agg({'target': 'count'})
users_active_conection.rename(
    columns = {'source': 'User name', 'target': 'Active network'}, inplace = True
)

users_passive_conection = network_df.groupby(by = 'target', as_index = False).agg({'source': 'count'})
users_passive_conection.rename(
    columns = {'target': 'User name', 'source': 'Passive network'}, inplace = True
)

user_activity = pd.merge(users_relevance, users_active_conection, how = 'left', left_on = 'User name', right_on = 'User name')
user_activity = pd.merge(user_activity, users_passive_conection, how = 'left', left_on = 'User name', right_on = 'User name')
user_activity.to_excel('User activity.xlsx')

