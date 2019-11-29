#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 10:31:13 2019

@author: geoffrey.kip
"""
import pandas as pd
import ast

##Read data in
df = pd.read_csv("../data/train.csv")
df.describe()
df.columns
df.dtypes

keep_columns = ['id', 'belongs_to_collection', 'budget', 'genres',
        'original_language', 'original_title', 'overview',
       'popularity', 'production_companies',
       'production_countries', 'release_date', 'runtime', 'spoken_languages',
       'status', 'tagline', 'title', 'Keywords', 'cast', 'crew', 'revenue']

df = df[keep_columns]
df.head(1)

#Transform dict columns
columnList = []
tempDF = pd.DataFrame()
def transform_dict(column):
    df[column] = df[column].fillna('[{}]')
    global columnList 
    global tempDF
    columnList = []
    for index,row in df[column].iteritems():
        columnStr= ''
        listofDict = ast.literal_eval(row)
        for dic in listofDict:
            if('name' in dic.keys()):
                columnStr=columnStr+';'+dic['name'] 
        columnStr=columnStr.strip(';') # trim leading ;
        columnList.append(columnStr)
    tempDF = pd.DataFrame(columnList,columns= [column])
    return tempDF

dict_cols = ['belongs_to_collection','genres','production_companies','production_countries','spoken_languages',
             'Keywords','cast','crew']

for col in df[dict_cols]:
    df[col] = transform_dict(col)
    
#Preprocessing
# Genres
df[['genre1','genre2','genre3','genre4','genre5','genre6','genre7']] = df.genres.str.split(";",expand=True)
df.drop(['genres'],inplace=True,axis=1)

# Companies
df[['prod_company1','prod_company2', 'prod_company3',
    'prod_company4','prod_company5','prod_company6','prod_company7','prod_company8',
    'prod_company9','prod_company10','prod_company11','prod_company12',
    'prod_company13','prod_company14','prod_company15','prod_company16','prod_company17']]= df.production_companies.str.split(";",expand=True)
df.drop(['production_companies'],inplace=True,axis=1)

#Countries
df[['prod_country1','prod_country2','prod_country3','prod_country4','prod_country5',
    'prod_country6','prod_country7','prod_country8']] = df.production_countries.str.split(";",expand=True)
df.drop(['production_countries'],inplace=True,axis=1)

#Languages
df[['language1','language2','language3','language4','language5',
    'language6','language7','language8','language9']] = df.spoken_languages.str.split(";",expand=True)
df.drop(['spoken_languages'],inplace=True,axis=1)

#Keywords
test_df = df.Keywords.str.split(";",expand=True)
test_df.columns = ['keyword_%i' % i for i in range(len(test_df.columns))]
#test_df.drop(['Keywords'],axis=1,inplace=True)
df = df.join(test_df)

#cast 
test_df = df.cast.str.split(";",expand=True)
test_df.columns = ['cast_%i' % i for i in range(len(test_df.columns))]
df= df.join(test_df)

#crew
test_df = df.crew.str.split(";",expand=True)
test_df.columns = ['crew_%i' % i for i in range(len(test_df.columns))]
df= df.join(test_df)