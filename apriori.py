# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 20:12:49 2021

@author: sasim
"""


import pandas as pd 
import pickle
df = pd.read_csv('D:\\sasi\\Metric Bees\\kz_new.csv')


df.info()





df.head(3)

def prepare_data(df):
    current_order_id = df.iloc[0,1]
    carts = []
    products = []
    for row in df.iterrows():
        order_id = row[1]['order_id']
        product_name = row[1]['category_code']
        if  order_id == current_order_id:
            products.append(product_name)
        else:
            carts.append(products)
            products = []
            products.append(product_name)
            current_order_id = order_id
    carts.append(products)
    
    return pd.DataFrame(carts)

carts_df = prepare_data(df)



transactions = []
for i in range(carts_df.shape[0]):
    transactions.append([str(carts_df.values[i,j]) for j in range(12)])
print(f'----Sameple cart ---- \n{transactions[0]}')


from apyori import apriori
rules = apriori(transactions= transactions, 
                min_support = 0.003, #Support shows transactions with items purchased together in a single transaction.
                min_confidence = 0.3, #Confidence shows transactions where the items are purchased one after the other.
                min_lift=3,
                min_length=2,
                max_length=7
               )
 

results = list(rules)
print(f'Number of Rules = {len(results)}')


print('----------- Sample rule --------------')
results[0]


def inspect(results):
    lhs         = [" + ".join(tuple(result[2][0][0])) for result in results]
    rhs         = [" + ".join(tuple(result[2][0][1])) for result in results]
    supports    = [result[1] for result in results]
    confidences = [result[2][0][2] for result in results]
    lifts       = [result[2][0][3] for result in results]
    return list(zip(lhs, rhs, supports, confidences, lifts))



resultsinDataFrame = pd.DataFrame(inspect(results), columns = ['product_name', 'Recommendation', 
                                                                'Support', 'Confidence', 'Lift'])
resultsinDataFrame.sort_values(by='Lift', ascending=False)


result = resultsinDataFrame[~resultsinDataFrame['product_name'].str.contains('electronics.video.tv', regex=False)].sort_values('Lift', ascending=False)[['Recommendation']].head(10)

da = str(input("enter"))

resultsinDataFrame[~resultsinDataFrame['product_name'].str.contains(da, regex=False)].sort_values('Lift', ascending=False)[['Recommendation']].head(10)


resultsinDataFrame.to_csv('D:\\sasi\\Metric Bees\\apriori\\apriori.csv',index=False)

pickle.dump(resultsinDataFrame, open('apriori_model.pkl','wb'))



resultsinDataFrame[~resultsinDataFrame['product_name'].str.contains('electronics.video.tv', regex=False)].sort_values('Lift', ascending=False)[['Recommendation']].head(10)

resultsinDataFrame[~resultsinDataFrame['In Cart'].str.contains('electronics.smartphone', regex=False)].sort_values('Lift', ascending=False)[['Recommendation']].head(10)


model[~model['Recommendation'].str.contains('electronics.video.tv', regex=False) & 
                   ~model['product_name'].str.contains('electronics.video.tv', regex=False)].sort_values('confidence', ascending=False).head(10)



filename = 'apriori_model.pkl'
model = pickle.load(open(filename, 'rb'))


def get_recommendations(title):
    
    filename = 'apriori_model.pkl'
    model = pickle.load(open(filename, 'rb'))
    
    data = (title)
    
    sim = model[~model['product_name'].str.contains(data, regex=False)].sort_values('Lift', ascending=False)[['Recommendation']]

    return model,sim


get_recommendations('electronics.video.tv')

d = model[~model['Recommendation'].str.contains('electronics.video.tv', regex=False) & 
                   ~model['product_name'].str.contains('electronics.video.tv', regex=False)].sort_values('Lift', ascending=False).head(10)




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

get_recommendations('electronics.video.tv')
