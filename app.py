from json_parser import JSONParser
import psycopg2
from psycopg2 import sql
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import os
import json

class StdOutListener(StreamListener):

    def on_data(self, data):

        parser = JSONParser(data)
        try:
            conn = psycopg2.connect(database="twitterdb", user="postgres", password="admin",port=5433)
        except:
            print("I am unable to connect to the database")

        cur = conn.cursor()
        try:
            for tweet in parser.createTweets(parser.data):
                try:
                    insert_user_row(tweet.user, cur)
                except:
                    pass

                try:
                    insert_tweet_row(tweet, cur)
                    for mentioned_user in tweet.mentioned_users:
                        insert_mentioned_user_row(mentioned_user, cur)
                    for hashtag in tweet.hashtags:
                        try:
                            insert_hashtag_row(hashtag, cur)
                            hashtag_id = fetch_hashtag_id(hashtag, cur)
                            insert_row_to_intersection_table(hashtag_id, tweet.id, cur)
                        except:
                            pass

                    conn.commit()
                except:
                    pass
        except:
            pass
        conn.commit()
        conn.close()
        return True

    def on_error(self, status):
        print(status)


def insert_user_row(user, cur):
    table_name = 'public.users(id, followers_count, location, name, screen_name, tweets_count, language)'
    cur.execute("insert into %s values (%%s, %%s, %%s, %%s, %%s, %%s, %%s)" % table_name,
                [user.id, user.followers_count, user.location, user.name, user.screen_name, user.tweets_count
                 , user.language])

def insert_tweet_row(tweet, cur):
    table_name = 'public.tweets(id, user_id, created_at, text, in_reply_tweet_id, in_reply_user_id, retweets_count)'
    cur.execute("insert into %s values (%%s, %%s, %%s, %%s, %%s, %%s, %%s)" % table_name,
                [tweet.id, tweet.user.id, tweet.created_at, tweet.text, tweet.in_reply_tweet_id, tweet.in_reply_user_id
                 , tweet.retweets_count])


def insert_mentioned_user_row(mentioned_user, cur):
    table_name = 'public.mentioned_users(tweet_id, user_id)'
    cur.execute("insert into %s values (%%s, %%s)" % table_name, [mentioned_user.tweet_id, mentioned_user.user_id])


def insert_hashtag_row(hashtag, cur):
    table_name = 'public.hashtags(name)'
    cur.execute("insert into %s values (%%s)" % table_name, [hashtag.name])


def fetch_hashtag_id(hashtag, cur):
    table_name = 'public.hashtags'
    cur.execute("select id from %s where name = %%s" % table_name, [hashtag.name])
    fetched_row = cur.fetchone()
    return fetched_row[0]


def insert_row_to_intersection_table(hashtag_id, tweet_id, cur):
    table_name = 'public.tweets_hashtags(hashtag_id, tweet_id)'
    cur.execute("insert into %s values (%%s, %%s)" % table_name, [hashtag_id, tweet_id])


def main():

    file = open('private_file_not_to_publish.txt', 'r')
    security_data = file.readlines()

    access_token = security_data[0].strip()
    access_token_secret = security_data[1].strip()
    consumer_key = security_data[2].strip()
    consumer_secret = security_data[3].strip()

    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['catalonia', 'catalunya',
                         'catalanindependence', 'catalonianreferendum'
                         'catalanreferendum2017', 'helpcatalonia'
                         'puigdemont', 'rajoy',  'savecatalonia',
                          'independenciaesp' , 'spanishdictatorship',
                         'KRLS', 'jcuixart', 'jordisanchezp'],async=True)



if __name__ == '__main__':
    main()