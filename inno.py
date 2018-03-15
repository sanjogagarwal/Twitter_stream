import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import time
import json
import pymongo
from pymongo import MongoClient

#keys_for_accessing_twitter
consumer_key = 'LmpjBvpnMojwainH4QyaCJqLL'
consumer_secret = 'm0BXDDLpIfgKFCgaAsctx2LrG0hwwT2WfBlHqOY4Sr6W9iA5GB'
access_token = '866637405373161474-h34OQgx1skciWFJnMzlAVXInJOGf9Ty'
access_secret = 'Sy1HKu12AzdQIU5NyjGhZeRmTMwER9V3MOIfY0c7kFtyS'

#accessing_twitter
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

#MongoDB_database_initialize
client = MongoClient('mongodb://localhost:27017')
db = client['twitter_db']
collection = db.users
 
class MyListener(StreamListener):
	def __init__(self, time_limit=60):
		self.start_time = time.time()
		self.limit = time_limit
		self.saveFile = open('python.json', 'a')
		super(MyListener, self).__init__()

	def on_data(self, data):
		if (time.time() - self.start_time) < self.limit:
			self.saveFile.write(data)
			self.saveFile.write('\n')
			tweet = json.loads(data)
			collection.insert(tweet)
			return True
		else:
			self.saveFile.close()
			return False

twitter_stream = Stream(auth, MyListener(time_limit=20))
twitter_stream.filter(track=['#goldenhobiday'])

for tweet in collection.find():
	print(tweet['text'])