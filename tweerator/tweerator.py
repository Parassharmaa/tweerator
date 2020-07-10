import csv
import sys
import time
import os
import tweepy
import json


class Tweerator(object):
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret, root_path='data'):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret

        self.access_token = access_token
        self.access_token_secret = access_token_secret

        self.auth = tweepy.OAuthHandler(
            self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(
            self.access_token, self.access_token_secret)

        self.auth = tweepy.OAuthHandler(
            self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True)
        self.root_path = root_path

    def load_state(self, keyword):
        id = ''
        print("Loading State...")
        if not os.path.isfile('status.json'):
            print("No State history found.")
            return ''
        
        status = json.load(open('status.json'))
        if status.get(keyword):
            print("\nFetching tweets for #{} from id {}".format(keyword, status[keyword]))
            id = status[keyword]
        else:
            print("\nFetching Tweets for #{}".format(keyword))
        print('-'*5)
        return id

    def save_state(self, keyword, since_id):
        if not os.path.isfile('status.json'):
            status = {
                keyword: since_id
            }
            json.dump(status, open('status.json', 'w'))
        else:
            status = json.load(open('status.json'))
            status[keyword] = since_id
            json.dump(status, open('status.json', 'w'))
        print("\n\nState Saved..")

    def init_csv(self, file_name):
        if not os.path.isdir(self.root_path):
            os.mkdir(self.root_path)

        data_path = "{}/{}.csv".format(self.root_path, file_name)
        file_exist = os.path.isfile(data_path)
        csv_file = csv.writer(open(data_path, 'a'))
        if not file_exist:
            csv_file.writerow(['created_at', 'username', 'tweet', 'source', 'geo'])
        return csv_file

    def fetch(self, keyword, count=100):
        file_name = "{}.csv".format(keyword)
        since_id = self.load_state(keyword)
        csv_file = self.init_csv(keyword)
        tc = 0
        ttc = 0
        t1 = time.time()
        tweet_id = since_id
        try:
            for tweet in tweepy.Cursor(self.api.search, q=keyword, count=count, lang="en", max_id=since_id).items():
                ttc += 1
                if (not tweet.retweeted) and ('RT @' not in tweet.text):
                    tc += 1
                    tweet_id = tweet.id
                    csv_file.writerow(
                        [tweet.created_at, tweet.user.screen_name, tweet.text.strip(), tweet.source, tweet.geo])
                    sys.stdout.write('''Tweets fetched: %d  \t Elapsed time: %d sec \t Efficiency: %d%%  \r''' % (
                        tc, round(time.time() - t1), round(5 * (ttc/(time.time()-t1)))))
                    sys.stdout.flush()
        except:
            sys.stdout.flush()
            self.save_state(keyword, tweet_id)
            print('-'*5)
            print("Tweets Fetched: {}".format(tc))
            print("Total Time: {} sec".format(round(time.time() - t1), 2))



    def download_tweets(self, ids_list):
        tweets_list = []

        for i, t_id in enumerate(ids_list):
            try:
                tweet = self.api.get_status(t_id)
                print(i)
                print(tweet.place)
                tweets_list.append(tweet._json)
            except:
                pass

        json.dump(tweets_list, open("tweets.json", 'w'))
