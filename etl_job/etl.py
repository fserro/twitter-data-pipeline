import pymongo
import time
from sqlalchemy import create_engine
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

time.sleep(10)  # seconds

# Establish a connection to the MongoDB server
client = pymongo.MongoClient("mongodb")

# Establish connection to Postgres
pg = create_engine('postgresql://postgres:1234@postgresdb:5432/tweets', echo=True)


def extract():
    db = client.tweets # Selects database 'tweets' in the MongoDB server
    collection = db.tweet_data # Selects the collection 'tweet_data' in database 'tweets'
    entries = collection.find()
    return entries

def transform(entries):
    s  = SentimentIntensityAnalyzer()
    unique_tweets = []
    unique_sentiments = []
    for e in entries:
        text = e['text']
        if text in unique_tweets:
            continue # skips retweets
        else:
            sentiment = s.polarity_scores(e['text'])
            score = sentiment['compound']
            unique_sentiments.append(score)
            unique_tweets.append(text)
    return unique_tweets, unique_sentiments

def load(uniques):
    pg.execute('''
    CREATE TABLE IF NOT EXISTS tweets (
    text VARCHAR(500),
    sentiment NUMERIC
);
''')
    pg.execute("TRUNCATE tweets;") # deletes all entries from the table to avoid duplicates
    for i in range(len(uniques[0])):
        query = "INSERT INTO tweets VALUES (%s, %s);"
        pg.execute(query, (uniques[0][i], uniques[1][i]))
    return None

#load(transform(extract())) 
while True:
    client = pymongo.MongoClient("mongodb")
    pg = create_engine('postgresql://postgres:1234@postgresdb:5432/tweets', echo=True)
    load(transform(extract())) 
    time.sleep(30)  # seconds

