# -*- coding: utf-8 -*-
"""saarthi.ai.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1o5W3srUTOaEIxTMbZDG12s139V6D-7rS

**IMPORTING ALL NECESSARY LIBRARIES**
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import nltk
from sklearn.preprocessing import LabelBinarizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from wordcloud import WordCloud,STOPWORDS
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize,sent_tokenize

"""**READING THE DATA**"""

train=pd.read_csv("/content/train_data.csv")
train.head()

valid=pd.read_csv("/content/valid_data.csv")
valid.head()

train['path'][0]

train['path'][1]

train['path']

"""**CHECKING FOR NULL VALUES**"""

train.isnull().any()

train['action'].unique()

action_list=['activate','deactivate','increase','decrease','change language','bring']
action_list

"""**UNIQUE VALUES IN THE DATASET**"""

train['object'].nunique()

train['object'].unique()

object_list=['lights', 'heat', 'Chinese', 'none', 'volume', 'English', 'lamp',
       'shoes', 'newspaper', 'socks', 'music', 'Korean', 'juice',
       'German']
object_list

train['location'].unique()

location_list=['kitchen', 'none', 'washroom', 'bedroom']
location_list

"""**DATA CLEANING**"""

import re
import string
from nltk.corpus import stopwords

def clean_text(text):
    """Process text function.
    Input:
        tweet: a string containing a tweet
    Output:
        tweets_clean: a list of words containing the processed tweet
    """
    lemmatizer = WordNetLemmatizer()
    stopwords_english = stopwords.words('english')
    text= re.sub('\[[^]]*\]', '', text)
    # remove stock market tickers like $GE
    text = re.sub(r'\$\w*', '', text)
    #removal of html tags
    review =re.sub(r'<.*?>',' ',text) 
    # remove old style retweet text "RT"
    text = re.sub(r'^RT[\s]+', '', text)
    # remove hyperlinks
    text = re.sub(r'https?:\/\/.*[\r\n]*', '', text)
    # remove hashtags
    # only removing the hash # sign from the word
    text = re.sub(r'#', '', text)
    text = re.sub("["
                           u"\U0001F600-\U0001F64F"  # removal of emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+",' ',text)
    text = re.sub('[^a-zA-Z]',' ',text) 
    text = text.lower()
    text_tokens =word_tokenize(text)

    text_clean = []
    for word in  text_tokens:
        if (                                       
            word not in string.punctuation):  # remove punctuation
            lem_word =lemmatizer.lemmatize(word)  # lemmitiging word
            text_clean.append(lem_word)
    text_mod=[i for i in text_clean if len(i)>1]
    text_clean=' '.join(text_mod)
    return  text_clean

import nltk
nltk.download('stopwords')

nltk.download('punkt')
nltk.download('wordnet')

train['clean_text']=train['transcription'].apply(lambda x: clean_text(x))

train['clean_text']

valid['clean_text']=valid['transcription'].apply(lambda x:clean_text(x))
valid['clean_text']

train['clean_text'][7]

valid.shape

train.shape

train.drop(['transcription','path'],axis=1,inplace=True)
train.shape

valid.drop(['transcription','path'],axis=1,inplace=True)
valid.shape

train.head()

train['labels']=train['action']+' '+train['object']+' '+train['location']
train.head()

valid.head()

valid['labels']=valid['action']+' '+valid['object']+' '+valid['location']
valid.head()

train.drop(['action','object','location'],axis=1,inplace=True)
train.head()

valid.drop(['action','object','location'],axis=1,inplace=True)
valid.head()

"""**TF-IDF VECTORIZATION**"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import metrics

vectorizer = TfidfVectorizer()
vectorised_train_documents = vectorizer.fit_transform(train["clean_text"])
vectorised_test_documents = vectorizer.transform(valid["clean_text"])

train_categories=train['labels']
train_categories.head()

test_categories=valid['labels']
test_categories.head()

"""**VECTORIZE OUTPUT LABELS**"""

from sklearn.preprocessing import MultiLabelBinarizer

mlb = MultiLabelBinarizer()
train_labels = mlb.fit_transform(train_categories)
test_labels = mlb.transform(test_categories)

train_labels

test_labels

"""**KNN MODEL**"""

from sklearn.neighbors import KNeighborsClassifier
from sklearn.multiclass import OneVsRestClassifier

knnClf = KNeighborsClassifier()

knnClf.fit(vectorised_train_documents, train_labels)
knnPredictions = knnClf.predict(vectorised_test_documents)
metricsReport("knn", test_labels, knnPredictions)

"""**RANDOM FOREST CLASSIFIER**"""

from sklearn.ensemble import RandomForestClassifier
rfClassifier = RandomForestClassifier(n_jobs=-1)
rfClassifier.fit(vectorised_train_documents, train_labels)
rfPreds = rfClassifier.predict(vectorised_test_documents)
metricsReport("Random Forest", test_labels, rfPreds)

"""**BAGGING CLASSIFIER**"""

from sklearn.ensemble import BaggingClassifier

bagClassifier = OneVsRestClassifier(BaggingClassifier(n_jobs=-1))
bagClassifier.fit(vectorised_train_documents, train_labels)
bagPreds = bagClassifier.predict(vectorised_test_documents)
metricsReport("Bagging", test_labels, bagPreds)

"""**GRADIENT BOOSTING CLASSIFIER**"""

from sklearn.ensemble import GradientBoostingClassifier

boostClassifier = OneVsRestClassifier(GradientBoostingClassifier())
boostClassifier.fit(vectorised_train_documents, train_labels)
boostPreds = boostClassifier.predict(vectorised_test_documents)
metricsReport("Boosting", test_labels, boostPreds)

