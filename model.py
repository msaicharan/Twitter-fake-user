import pandas as pd
import sklearn as skl
import numpy as np
import nltk
import sys
nltk.download('stopwords')
from nltk.corpus import stopwords
import riidl_final
import tweepy
import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

print ("fvvdfvf")

CONSUMER_KEY = 'gejfWul5iUg3qKQfSDiYzvkyn'
CONSUMER_SECRET = 'pu0YscYt1vJvKS714fnMRL8oxC1NGpvzjXT1hVyfJ6X6WuE7NC'
ACCESS_KEY = '1027969527714336768-d9zUk6g67A1B6yve4ZZ6QIqD5mDtic'
ACCESS_SECRET = 'FP2nrfJ7v7NHezSvt9u1uR6YoHgPnmm6ip0mALUprTYrB'

class TweetListener(StreamListener):

    # A listener handles tweets are the received from the stream.
    #This is a basic listener that just prints received tweets to standard output

    def on_data(self, data):
        print (data)
        return True

    def on_error(self, status):
        print (status)


auth = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
api = tweepy.API(auth)

auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
twitterStream = Stream(auth,TweetListener())

if(api.verify_credentials):
    print ('We successfully logged in')

print(sys.argv[1])
user = api.get_user(sys.argv[1])



if(user.statuses_count!=0):
	try:
		for status in tweepy.Cursor(api.user_timeline, screen_name=user.screen_name).items():
			status = (status._json['text'])
	except Exception as e:
		status  = "Exception occured"
else:
	status = 'none'

data = {'User_screen_name': user.screen_name , 'Description':user.description, '#_Followers':user.followers_count, '#_Following':user.friends_count, 'statuses_count':user.statuses_count, '#_favourites_count': user.favourites_count, 'default_profile': user.default_profile,'default_profile_image': user.default_profile_image, 'verified':user.verified,'status.text':status }

df = pd.DataFrame(data,index=[0])
print(df['Description'])

A = df['#_Followers'].values
B = df['#_Following'].values
C=  df['statuses_count'].values
D = df['#_favourites_count'].values

#For description

if(df['Description'].values != 0):
  E = df['Description'].apply(lambda x: len(str(x).split(" ")))

  F = df['Description'].str.len()

  if(F.values != 0):
    def avg_word(sentence):
      words = sentence.split()
      return (sum(len(word) for word in words)/len(words))

    G = df['Description'].apply(lambda x: avg_word(x))

    stop = stopwords.words('english')
    H = df['Description'].apply(lambda x: len([x for x in x.split() if x in stop]))

  else:
    G = 0
    H = 0
    
else:
  E = 0
  F = 0
  G = 0
  H = 0

#For "default_profile":
if(np.array_equal(df['default_profile'], [0,'True'])):
    I = 0
else:
    I = 1

#For "default_profile_image"
if(np.array_equal(df['default_profile_image'], [0,'True'])):
    J = 1
else:
    J = 0

#For verified
if(np.array_equal(df['verified'], [0,'False'])):
    K = 1
else:
    K = 0

# For status

if(status!='none'):
  L = df['status.text'].apply(lambda x: len(str(x).split(" ")))

  M = df['status.text'].str.len()

  N = df['status.text'].apply(lambda x: avg_word(x))

  stop1 = stopwords.words('english')
  O = df['status.text'].apply(lambda x: len([x for x in x.split() if x in stop1]))

else:
  L = 0
  M = 0
  N = 0
  O = 0
  
#Following follower ratio
P = B/A

if(P>99999):
  P = 99999




# predict the response for a new observation
VAL = knn.predict([[A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P]])

if(VAL==1):
  print("User is GENUINE")
else:
  print("User is FAKE")





