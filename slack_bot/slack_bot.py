import requests
import time
from sqlalchemy import create_engine
import logging

WEBHOOK_URL = "https://hooks.slack.com/services/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" 
logging.basicConfig(level='DEBUG', filename='slacked_tweets.txt', 
                    format='%(asctime)s | THESE TWEETS WERE ALREADY SLACKED: %(message)s',
                    force=True)

time.sleep(120) # seconds

slacked_tweets = []
while len(slacked_tweets) < 50:
    pg = create_engine('postgresql://postgres:1234@postgresdb:5432/tweets', echo=True) # connects to postgres

    # extract happy tweet
    happy_text_query = '''
    SELECT text FROM tweets ORDER BY sentiment DESC;
    '''
    happy_sent_query = '''
    SELECT sentiment FROM tweets ORDER BY sentiment DESC;
    '''

    happy_tweets = list(pg.execute(happy_text_query))
    happy_sentiments = list(pg.execute(happy_sent_query))

    for i, tweet in enumerate(happy_tweets):
        if tweet[0] not in slacked_tweets:
            text = '\U0001F603' * 15 + '\n'
            text += 'There is a new HAPPY tweet about vanilla:\n\n\n' + tweet[0] + '\n\n\nwith a sentiment value of ' + str(happy_sentiments[i][0])
            text += '\n' + '\U0001F603' * 15
            json_bot = {'text': text}
            requests.post(url=WEBHOOK_URL, json = json_bot)
            slacked_tweets.append(tweet[0])
            break
        else:
            continue

    time.sleep(60)

    # extract sad tweet
    sad_text_query = '''
    SELECT text FROM tweets ORDER BY sentiment ASC;
    '''
    sad_sent_query = '''
    SELECT sentiment FROM tweets ORDER BY sentiment ASC;
    '''

    sad_tweets = list(pg.execute(sad_text_query))
    sad_sentiments = list(pg.execute(sad_sent_query))

    for i, tweet in enumerate(sad_tweets):
        if tweet[0] not in slacked_tweets:
            text = '\U00002639' * 15 + '\n'
            text += 'There is a new SAD tweet about vanilla:\n\n\n' + tweet[0] + '\n\n\nwith a sentiment value of ' + str(sad_sentiments[i][0])
            text += '\n' + '\U00002639' * 15
            json_bot = {'text': text}
            requests.post(url=WEBHOOK_URL, json = json_bot)
            slacked_tweets.append(tweet[0])
            break
        else:
            continue
    
    logging.debug(msg = slacked_tweets)
    time.sleep(300)

