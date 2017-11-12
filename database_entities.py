class Hashtag:
    name = None

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class MentionedUser:
    user_id = None
    tweet_id = None

    def __init__(self, user_id, tweet_id):
        self.user_id = user_id
        self.tweet_id = tweet_id

class User:
    id = None
    followers_count = None
    location = None
    name = None
    screen_name = None
    tweets_count = None
    language = None

    def __init__(self, id, followers_count, location, name, screen_name, tweets_count, language):
        self.id = id
        self.followers_count = followers_count
        self.location = location
        self.name = name
        self.screen_name = screen_name
        self.tweets_count = tweets_count
        self.language = language

class Tweet:
    hashtags = []
    mentioned_users = []
    user = None

    id = None
    created_at = None
    text = None
    in_reply_tweet_id = None
    in_reply_user_id = None
    retweets_count = None

    def __init__(self, hashtags, mentioned_users, user, id, created_at, text, in_reply_tweet_id, in_reply_user_id,
                 retweets_count):
        self.hashtags = hashtags
        self.mentioned_users = mentioned_users
        self.user = user
        self.id = id
        self.created_at = created_at
        self.text = text
        self.in_reply_tweet_id = in_reply_tweet_id
        self.in_reply_user_id = in_reply_user_id
        self.retweets_count = retweets_count