# twitter-data-pipeline
Twitter Sentiment Analysis &amp; Data Pipeline

Docker pipeline tweet streamer in Python. Tweets mentioning the term 'vanilla' are detected in real time with Tweepy and stored in a MongoDB database; ETL job and sentiment analysis using Vader; resulting analysis stored in a PostgreSQL database and posted to a Slack channel with a slackbot.
