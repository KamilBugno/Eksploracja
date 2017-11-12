import json
import re
from database_entities import *

class JSONParser:

    data = None

    def __init__(self, data):
        self.data = self.parse_json(data)

    def parse_json(self, data):
        # with open('test.json', 'r') as data_file:
        #     return json.load(data_file)
        return list(self.iterparse(data))

    def iterparse(self, data):
        nonspace = re.compile(r'\S')
        decoder = json.JSONDecoder()
        pos = 0
        string_data = data
        while True:
            matched = nonspace.search(string_data, pos)
            if not matched:
                break
            pos = matched.start()
            decoded, pos = decoder.raw_decode(string_data, pos)
            yield decoded

    def get_hashtags(self, tweet):
        hashtag_list = []
        for hashtag in tweet["entities"]["hashtags"]:
            hashtag_list.append(Hashtag(hashtag["text"]))
        return hashtag_list

    def get_user_mentions(self, tweet):
        mentioned_users = []
        for mentioned_user in tweet["entities"]["user_mentions"]:
            mentioned_users.append(MentionedUser(mentioned_user["id"], tweet["id"]))
        return mentioned_users

    def get_user(self, tweet):
        user = tweet["user"]
        return User(user["id"], user["followers_count"], user["location"], user["name"], user["screen_name"], user["statuses_count"],
                    user["lang"])

    def createTweets(self, tweets):
        tweets_to_db = []
        for tweet in tweets:
            text = tweet["text"]
            if "\u2026" in text:
                #print("________________________")
                text = tweet["retweeted_status"]["extended_tweet"]["full_text"]
            tweets_to_db.append(Tweet(self.get_hashtags(tweet), self.get_user_mentions(tweet), self.get_user(tweet), tweet["id"],
                                      tweet["created_at"], text, tweet["in_reply_to_status_id"], tweet["in_reply_to_user_id"],
                                      tweet["retweet_count"]))
        return tweets_to_db
