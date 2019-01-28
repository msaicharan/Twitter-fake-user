import pandas as pd
import sklearn as skl
import numpy as np
import nltk
import xlrd

nltk.download('stopwords')

from nltk.corpus import stopwords

df = pd.read_csv("kj_copy.csv")

ff_ratio = (df['#_Following']/df['#_Followers'])

b =[]

for i in range(0,len(df)):
  if(df.verified[i]=="True"):
    b.append(1)
  else:
    b.append(0)

df['word_count'] = df['Description'].apply(lambda x: len(str(x).split(" ")))
df1 = df[['word_count','Description']]



"""**CHARACTER COUNT:**"""

df['char_count'] = df['Description'].str.len() ## this also includes spaces

df['char_count'] = df['char_count'].fillna(0)

df = df.fillna('NULL')

"""**AVERAGE WORD LENGTH:**"""

#if(df['char_count'].values != 0)

def avg_word(sentence):
  words = sentence.split()
  return (sum(len(word) for word in words)/len(words))

df['avg_word'] = df['Description'].apply(lambda x: avg_word(x))
 

"""**NUMBER OF STOPWORDS:**"""

stop = stopwords.words('english')

df['stopwords'] = df['Description'].apply(lambda x: len([x for x in x.split() if x in stop]))


"""**CONVERTING TRUE/FALSE TO 1/0:**"""

#For "verified":
v =[]

for i in range(0,len(df)):
  if(df.verified[i]== True):
    v.append(1)
  else:
    v.append(0)


#For "default_profile":
dp =[]

for i in range(0,len(df)):
  if(df.default_profile[i]== True):
    dp.append(1)
  else:
    dp.append(0)


#For "default_profile_image"
dpi =[]

for i in range(0,len(df)):
  if(df.default_profile_image[i]== True):
    dpi.append(1)
  else:
    dpi.append(0)


#Adding these to the dataframe:
data = {'User_screen_name': df.User_screen_name,
        'verified_binary': v,
        'default_profile_binary': dp,
        'default_profile_image_binary': dpi
       }

df2 = pd.DataFrame(data)
df = pd.merge(df, df2, on="User_screen_name")


status = []

for index,row in df.iterrows():
  if(row['status.text'] != 'none'):
    status.append(df.loc[index]['status.text'])
  else:
    status.append(None)
      
#Adding this to the dataframe:
data = {'User_screen_name': df.User_screen_name,
        'status': status,
       }

df3 = pd.DataFrame(data)
df = pd.merge(df,df3,on="User_screen_name")


"""**STATUS WORD COUNT:**"""

df['status_word_count'] = df['status'].apply(lambda x: len(str(x).split(" ")))

df1 = df[['status_word_count','status']]


"""**STATUS CHARACTER COUNT:**"""

df['status_char_count'] = df['status'].str.len() ## this also includes spaces


"""**STATUS AVERAGE WORD LENGTH**"""

def avg_word(sentence):
  words = sentence.split()
  return (sum(len(word) for word in words)/len(words))

df['status_avg_word'] = df['status.text'].apply(lambda x: avg_word(x))


"""**STATUS NUMBER OF STOPWORDS: **"""

stop = stopwords.words('english')

df['status_stopwords'] = df['status.text'].apply(lambda x: len([x for x in x.split() if x in stop]))

"""#Creating the final numeric dataset:"""

#Adding these to the dataframe:
data = {'User_screen_name': df.User_screen_name,
        'ff_ratio': ff_ratio
       }

df2 = pd.DataFrame(data)
df = pd.merge(df,df2,on="User_screen_name")

df_final = df[['#_Followers', '#_Following', 'statuses_count', '#_favourites_count', 'word_count', 'char_count', 'avg_word', 'stopwords', 'default_profile_binary', 'default_profile_image_binary', 'verified_binary', 'status_word_count', 'status_char_count', 'status_avg_word', 'status_stopwords', 'ff_ratio']]


#REFINING:
df['status_char_count'] = df['status_char_count'].fillna(0)

ff = []

for i in range(0,len(df)):
  if(df.ff_ratio[i] > 999999):
    ff.append(99999)
  else:
    ff.append(df.ff_ratio[i])


data = {'User_screen_name': df.User_screen_name,
        'ff_ratio_final': ff,
       }

df5 = pd.DataFrame(data)
df = pd.merge(df,df5,on="User_screen_name")

"""# Implementing Classifier:"""

a = df['#_Followers'].values
b = df['#_Following'].values
c = df['statuses_count'].values
d = df['#_favourites_count'].values
e = df['word_count'].values
f = df['char_count'].values
g = df['avg_word'].values
h = df['stopwords'].values
i = df['default_profile_binary'].values
j = df['default_profile_image_binary'].values
k = df['verified_binary'].values
l = df['status_word_count'].values
m = df['status_char_count'].values
n = df['status_avg_word'].values
o = df['status_stopwords'].values
p = df['ff_ratio_final'].values
X = np.array([a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p])
X = X.transpose()

xl = pd.ExcelFile("label.xlsx")
df1 = xl.parse('Sheet1')
y = np.array([df1['Label'].values])
y = y.transpose()
y = y.ravel()

"""# ***KNN Classifier:***"""

# import the class
from sklearn.neighbors import KNeighborsClassifier
# instantiate the model (with the default parameters)
knn = KNeighborsClassifier()

# fit the model with data (occurs in-place)
knn.fit(X, y)


