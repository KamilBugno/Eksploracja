import psycopg2
from sentiment_analysis import SentimentAnalysis

# CREATE TABLE public.one
# (
#     id bigint NOT NULL,
#     a bigint,
#     b bigint,
#     CONSTRAINT one_pkey PRIMARY KEY (id)
# )
# WITH (
#     OIDS = FALSE
# )
# TABLESPACE pg_default;
#
# ALTER TABLE public.one
#     OWNER to postgres;

# Klasa ta jest prototypem klasy do obliczania dla kazdego wiersza sentymentu i uaktualniania bazy
class Updater():
    def connect_to_database(self):
        try:
            conn = psycopg2.connect(database="twitterdb", user="postgres", password="admin", port=5433)
        except:
            print("I am unable to connect to the database")
        return conn

    def select_data_from_database(self, conn):
        cur = conn.cursor()
        cur.execute("select user_id, text from tweets inner join users "
                    "on users.id = tweets.user_id where users.language = 'en'")
        return cur.fetchall() # gdy danych bedzie mnostwo, wtedy moga byc problemy z pamiecia

    def update(self, text):
        sa = SentimentAnalysis()
        cleaned_text = sa.clean_text_tweet_from_mails_and_rubbish(text)
        return  sa.get_tweet_sentiment(cleaned_text)

    def update_data(self, rows, conn):
        for row in rows:
            r_list = list(row)
            self.insert_data_to_database(conn, r_list[0], self.update(r_list[1]))
        return

    def insert_data_to_database(self, conn, id, new_value):
        cur = conn.cursor()
        cur.execute("UPDATE tweets SET sentiment_polarity = %s WHERE user_id = %s", (new_value, id))
        conn.commit()


def main():
    updater = Updater()
    conn = updater.connect_to_database()
    rows = updater.select_data_from_database(conn)
    updater.update_data(rows, conn)

if __name__ == '__main__':
    main()


