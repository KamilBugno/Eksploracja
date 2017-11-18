from textblob import TextBlob
import re

class SentimentAnalysis:

    def clean_text_tweet_from_mails_and_rubbish(self, tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def get_tweet_sentiment(self, text):
        analysis = TextBlob(self.clean_text_tweet_from_mails_and_rubbish(text))
        return analysis.sentiment.polarity
        # if analysis.sentiment.polarity > 0:
        #     return 'positive'
        # elif analysis.sentiment.polarity == 0:
        #     return 'neutral'
        # else:
        #     return 'negative'

def main():
     sentiment = SentimentAnalysis()
     print(sentiment.get_tweet_sentiment("i love it"))

if __name__ == '__main__':
    main()