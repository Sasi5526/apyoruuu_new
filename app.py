# -*- coding: utf-8 -*-
"""
Created on Fri Jul  2 10:57:43 2021

@author: sasim
"""


import pandas as pd
from flask import Flask,render_template, request
import pickle

def get_recommendations(m):
    filename = 'apriori_model.pkl'
    model = pickle.load(open(filename, 'rb'))
    m = m.lower()
    #Check if the movie is in our database or not
    if m not in model['product_name'].unique():
        return('This product is not in our database.\n Please spell check or enter a different product name')
    else:
        #getting the index of the movie in the dataframe
        i = model.loc[model['product_name']==m].index[0]
        #fetching the row containing the similarity score of the movie
        # from similarity matrix and enumerating over it.
        lst = model[~model['product_name'].str.contains(m, regex=False)].sort_values('Lift', ascending=False)[['Recommendation']]
        #Taking top 10 movies
        #Ignoring the first index as it is the original movie
        lst = lst[1:11]
        #Making an empty list containing all 10 movie recommendations
        l= []
        for i in range(len(lst)):
            l.append(lst.iloc[i][0])
        return l

app = Flask(__name__)
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/recommend")
def recommend():
    product_name = request.args.get('product_name')
    r = get_recommendations(product_name)
    product_name = product_name.upper()
    if type(r) == type('string'):
        return render_template('recommend.html',product_name=product_name,r=r,t='s')
    else:
        return render_template('recommend.html',product_name=product_name,r=r,t='l')
    
if __name__ == '__main__':
    app.run()
