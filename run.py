from tweerator import Tweerator


consumer_key = ""
consumer_secret = ""

access_token = ""
access_token_secret = ""


ts = Tweerator(consumer_key, consumer_secret,
               access_token, access_token_secret)

ts.fetch("hello")
