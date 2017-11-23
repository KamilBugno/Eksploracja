import numpy as np
import matplotlib.pyplot as plt
import psycopg2

class Analyzer():
    def connect_to_database(self):
        try:
            conn = psycopg2.connect(database="twitterdb", user="postgres", password="admin", port=5433)
        except:
            print("I am unable to connect to the database")
        return conn

    def select_top_5_language(self, conn):
        cur = conn.cursor()
        cur.execute("Select users.language, count(*) as amount from users "
                    "group by users.language order by amount desc")
        return cur.fetchall()

    def count_positive_sentiment_polarity(self, conn):
        cur = conn.cursor()
        cur.execute("Select count(*) as amount from tweets where sentiment_polarity > 0")
        return cur.fetchall()

    def count_neutral_sentiment_polarity(self, conn):
        cur = conn.cursor()
        cur.execute("Select count(*) as amount from tweets where sentiment_polarity = 0")
        return cur.fetchall()

    def count_negative_sentiment_polarity(self, conn):
        cur = conn.cursor()
        cur.execute("Select count(*) as amount from tweets where sentiment_polarity < 0")
        return cur.fetchall()

    def count_null_sentiment_polarity(self, conn):
        cur = conn.cursor()
        cur.execute("Select count(*) as amount from tweets where sentiment_polarity is null")
        return cur.fetchall()

    def draw_sentiment_analysis_with_null(self, conn):
        positive = self.count_positive_sentiment_polarity(conn)
        negative = self.count_negative_sentiment_polarity(conn)
        neutral = self.count_neutral_sentiment_polarity(conn)
        null_sentiment = self.count_null_sentiment_polarity(conn)

        status = ['calculated sentiment', 'not calculated sentiment']
        frequency = []

        frequency.append(positive[0][0]+negative[0][0]+neutral[0][0])
        frequency.append(null_sentiment[0][0])

        indices = np.arange(2)
        plt.bar(indices, frequency, color='r')
        plt.xticks(indices, status, rotation='vertical')
        plt.tight_layout()
        plt.show()

    def draw_sentiment_analysis(self, conn):
        positive = self.count_positive_sentiment_polarity(conn)
        negative = self.count_negative_sentiment_polarity(conn)
        neutral = self.count_neutral_sentiment_polarity(conn)

        status = ['positive', 'neutral', 'negative']
        frequency = []

        frequency.append(positive[0][0])
        frequency.append(negative[0][0])
        frequency.append(neutral[0][0])

        indices = np.arange(3)
        plt.bar(indices, frequency, color='r')
        plt.xticks(indices, status, rotation='vertical')
        plt.tight_layout()
        plt.show()

    def draw_top_5_language(self, data):
        language = []
        frequency = []

        for i in range(len(data[:5])):
            language.append(data[i][0])
            frequency.append(data[i][1])

        language.append('other')
        amount = 0
        for i in range(len(data[-(len(data)-5):])):
            amount += data[i+5][1]

        frequency.append(amount)

        indices = np.arange(6)
        plt.bar(indices, frequency, color='r')
        plt.xticks(indices, language, rotation='vertical')
        plt.tight_layout()
        plt.show()

def main():
    analyzer = Analyzer()
    conn = analyzer.connect_to_database()
    data = analyzer.select_top_5_language(conn)
    analyzer.draw_top_5_language(data)
    analyzer.draw_sentiment_analysis_with_null(conn)
    analyzer.draw_sentiment_analysis(conn)

if __name__ == '__main__':
    main()
