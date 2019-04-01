## Simply Machine Learning script to predict pagename from page content
## Will be used to import Quora answers into ThoughtStorms Wiki

# -*- coding: utf-8 -*-

from fsquery import FSQuery
import csv
import random

pages_path = "/home/phil/Documents/new_dev_tree/writing/thoughtstorms/pages/"
fsq = FSQuery(pages_path).Ext("md").NoFollow(".work").NoFollow(".git").FileOnly()

NO_SELECTIONS = 5
                
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
        
def filter_line(x) :
    if x == "" : return False
    if x == "\n" : return False
    if not x.strip() : return False
    if len(x) < 10 : return False
    if x[0:9] == "#redirect" : return False
    if x[0:6] == "*added" : return False
    if x[0:12] == "*originally*" : return False
    if "{=linkbin=}" in x : return False    

    if x[0:11] == "### linkbin" : return False
    if x[0:10] == "can't find" : return False

    return True

def remove_stops(x) :
    x = x.strip()
    xs = x.split(" ")
    xs = [x.lower() for x in xs if not x.lower() in ENGLISH_STOP_WORDS]
    return " ".join(xs)

def random_sample_of_lines(xs) :
    return [x for x in xs if random.randint(1,1000) < 500]

with open("out.csv",mode="w") as out :
    writer = csv.writer(out)

    writer.writerow(["Line","Page"])
    for n in fsq :
        name = (n.abs.split("/")[-1]).split(".")[0]
        f = n.open_file()
        lines = [remove_stops(x) for x in f.readlines() if filter_line(remove_stops(x))]
        
        for i in range(NO_SELECTIONS) :
            sample = " ".join(random_sample_of_lines(lines))
            writer.writerow([sample,name])

        
"""
with open("out.csv") as inn :
    reader = csv.reader(inn)
    for row in reader :
        print row[0]
        print row[1]
"""        
        
import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("out.csv")
print df.head()

train, test = train_test_split(df, test_size=0.2, random_state=42)
print('Sample Line', train['Line'].iloc[0])
print('Sample Page Name', train['Page'].iloc[0])
print('Training Data Shape:', train.shape)
print('Testing Data Shape:', test.shape)

from nltk.corpus import stopwords  
from sklearn.feature_extraction.text import CountVectorizer  

train_texts = train[train.Line.notnull()]
train_texts = train_texts["Line"].tolist()

test_texts = test[test.Line.notnull()]
test_texts = test_texts["Line"].tolist()

#print train_texts
#print "_________________________________"
#print test_texts

vectorizer = CountVectorizer(decode_error='ignore',max_features=2500)  
vectorizer.fit(train_texts)

#print vectorizer.vocabulary_


print vectorizer.transform(train_texts).toarray()





