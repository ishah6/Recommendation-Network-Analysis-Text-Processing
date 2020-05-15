# -*- coding: utf-8 -*-
"""
@author: hina & ishani
"""
print ()

import networkx
from operator import itemgetter
import matplotlib.pyplot
import pandas as pd
import math


# Read the data from amazon-books.csv into amazonBooks dataframe;
amazonBooks = pd.read_csv('./amazon-books.csv', index_col=0)

# Read the data from amazon-books-copurchase.adjlist;
# assign it to copurchaseGraph weighted Graph;
# node = ASIN, edge= copurchase, edge weight = category similarity
fhr=open("amazon-books-copurchase.edgelist", 'rb')
copurchaseGraph=networkx.read_weighted_edgelist(fhr)
fhr.close()

# Now let's assume a person is considering buying the following book;
# what else can we recommend to them based on copurchase behavior 
# we've seen from other users?
print ("Looking for Recommendations for Customer Purchasing this Book:")
print ("--------------------------------------------------------------")
purchasedAsin = '0805047905'

# Let's first get some metadata associated with this book
print ("ASIN = ", purchasedAsin) 
print ("Title = ", amazonBooks.loc[purchasedAsin,'Title'])
print ("SalesRank = ", amazonBooks.loc[purchasedAsin,'SalesRank'])
print ("TotalReviews = ", amazonBooks.loc[purchasedAsin,'TotalReviews'])
print ("AvgRating = ", amazonBooks.loc[purchasedAsin,'AvgRating'])
print ("DegreeCentrality = ", amazonBooks.loc[purchasedAsin,'DegreeCentrality'])
print ("ClusteringCoeff = ", amazonBooks.loc[purchasedAsin,'ClusteringCoeff'])
    

# Now let's look at the ego network associated with purchasedAsin in the
# copurchaseGraph - which is esentially comprised of all the books 
# that have been copurchased with this book in the past
# (1) YOUR CODE HERE: 
#     Get the depth-1 ego network of purchasedAsin from copurchaseGraph,
#     and assign the resulting graph to purchasedAsinEgoGraph.
#purchasedAsinEgoGraph = networkx.Graph()
purchasedAsinEgoGraph = networkx.Graph(networkx.ego_graph(copurchaseGraph, purchasedAsin, radius=1))

# Next, recall that the edge weights in the copurchaseGraph is a measure of
# the similarity between the books connected by the edge. So we can use the 
# island method to only retain those books that are highly simialr to the 
# purchasedAsin
# (2) YOUR CODE HERE: 
#     Use the island method on purchasedAsinEgoGraph to only retain edges with 
#     threshold >= 0.5, and assign resulting graph to purchasedAsinEgoTrimGraph
threshold = 0.5
purchasedAsinEgoTrimGraph = networkx.Graph()
for n1, n2, edge in purchasedAsinEgoGraph.edges(data=True):
    if edge['weight'] >= threshold:
        purchasedAsinEgoTrimGraph.add_edge(n1,n2,weight=edge['weight'])

# Next, recall that given the purchasedAsinEgoTrimGraph you constructed above, 
# you can get at the list of nodes connected to the purchasedAsin by a single 
# hop (called the neighbors of the purchasedAsin) 
# (3) YOUR CODE HERE: 
#     Find the list of neighbors of the purchasedAsin in the 
#     purchasedAsinEgoTrimGraph, and assign it to purchasedAsinNeighbors
#purchasedAsinNeighbors = []
purchasedAsinNeighbors = [n for n in purchasedAsinEgoTrimGraph.neighbors(purchasedAsin)]

# Next, let's pick the Top Five book recommendations from among the 
# purchasedAsinNeighbors based on one or more of the following data of the 
# neighboring nodes: SalesRank, AvgRating, TotalReviews, DegreeCentrality, 
# and ClusteringCoeff
# (4) YOUR CODE HERE: 
#     Note that, given an asin, you can get at the metadata associated with  
#     it using amazonBooks (similar to lines 29-36 above).
#     Now, come up with a composite measure to make Top Five book 
#     recommendations based on one or more of the following metrics associated 
#     with nodes in purchasedAsinNeighbors: SalesRank, AvgRating, 
#     TotalReviews, DegreeCentrality, and ClusteringCoeff. Feel free to compute
#     and include other measures if you like.
#     YOU MUST come up with a composite measure.
#     DO NOT simply make recommendations based on sorting!!!
#     Also, remember to transform the data appropriately using 
#     sklearn preprocessing so the composite measure isn't overwhelmed 
#     by measures which are on a higher scale.
purchasedAsinNeighbors_Title=[]
purchasedAsinNeighbors_SalesRank=[]
purchasedAsinNeighbors_TotalReviews=[]
purchasedAsinNeighbors_AvgRating=[]
purchasedAsinNeighbors_DegreeCentrality=[]
purchasedAsinNeighbors_ClusteringCoeff=[]

for n in purchasedAsinNeighbors:
        purchasedAsinNeighbors_Title.append((n,amazonBooks.loc[n,'Title']))
        purchasedAsinNeighbors_SalesRank.append((n,amazonBooks.loc[n,'SalesRank']))
        purchasedAsinNeighbors_TotalReviews.append((n,amazonBooks.loc[n,'TotalReviews']))
        purchasedAsinNeighbors_AvgRating.append((n,amazonBooks.loc[n,'AvgRating']))
        purchasedAsinNeighbors_DegreeCentrality.append((n,amazonBooks.loc[n,'DegreeCentrality']))
        purchasedAsinNeighbors_ClusteringCoeff.append((n,amazonBooks.loc[n,'ClusteringCoeff']))

list_SR=[]
for n in range(len(purchasedAsinNeighbors_SalesRank)): 
    list_SR.append((purchasedAsinNeighbors_SalesRank[n][0],
              purchasedAsinNeighbors_SalesRank[n][1]+2.00000))
print ("list_SR = ", list_SR)

list_TR=[]
for n in range(len(purchasedAsinNeighbors_TotalReviews)): 
    list_TR.append((purchasedAsinNeighbors_TotalReviews[n][0],
              purchasedAsinNeighbors_TotalReviews[n][1]+2.00000))
print ("list_TR = ", list_TR)  

list_DC=[]
for n in range(len(purchasedAsinNeighbors_DegreeCentrality)): 
    list_DC.append((purchasedAsinNeighbors_DegreeCentrality[n][0],
              purchasedAsinNeighbors_DegreeCentrality[n][1]+2.00000))
print ("list_DC = ", list_DC) 

list_CC=[]
for n in range(len(purchasedAsinNeighbors_ClusteringCoeff)): 
    list_CC.append((purchasedAsinNeighbors_ClusteringCoeff[n][0],
              purchasedAsinNeighbors_ClusteringCoeff[n][1]*5))
print ("list_CC = ", list_CC) 

c_score=[]
for n in range(len(purchasedAsinNeighbors_AvgRating)):
    c_score.append((purchasedAsinNeighbors_AvgRating[n][0],
                    list_TR[n][1] 
                    + purchasedAsinNeighbors_AvgRating[n][1] 
                    - list_SR[n][1] 
                    + list_DC[n][1]
                    + list_CC[n][1] 
                    )) 
print ("c_score = ", c_score)

# Print Top 5 recommendations (ASIN, and associated Title, Sales Rank, 
# TotalReviews, AvgRating, DegreeCentrality, ClusteringCoeff)
# (5) YOUR CODE HERE:  
def sort_desc(x):
    return x[1]
score_sorted=sorted(c_score,key=sort_desc,reverse=True)
print ("score_sorted = ", score_sorted)

top_list=[]
for n in range(5):
    top_list.append(score_sorted[n])   
print ("top_list = ", top_list) 

for n in top_list:
    purchasedAsin=n[0] 
    print ("ASIN = ", purchasedAsin) 
    print ("Title = ", amazonBooks.loc[purchasedAsin,'Title'])
    print ("SalesRank = ", amazonBooks.loc[purchasedAsin,'SalesRank'])
    print ("TotalReviews = ", amazonBooks.loc[purchasedAsin,'TotalReviews'])
    print ("AvgRating = ", amazonBooks.loc[purchasedAsin,'AvgRating'])
    print ("DegreeCentrality = ", amazonBooks.loc[purchasedAsin,'DegreeCentrality'])
    print ("ClusteringCoeff = ", amazonBooks.loc[purchasedAsin,'ClusteringCoeff'])
