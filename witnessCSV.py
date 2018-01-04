# -*- coding: utf-8 -*-

from steem import Steem
from steem.account import Account
import pandas as pd
import os
import plotly
import math
plotly.tools.set_credentials_file(username='plotlyusername', api_key='plotlyapikey')

#####
#Set Directory
####

targetDirectory=('/Users/Jared/SD')

os.chdir(targetDirectory)

#####
#Set Steem Instance and pull list of active witnesses
#Tests connection by printing sbd balance and list of active witnesses
####
    
s = Steem()
witnessDf=pd.DataFrame(s.get_witnesses_by_vote('',30))
witnesses = witnessDf['owner'].tolist()
print(s.get_account('jaredcwillis')['sbd_balance'])
print(witnesses)
selfVoteslist=[]
totalVoteslist=[]
#####
#Pulls voting lists for active witnesses
####

for currentWitness in witnesses:
    print(currentWitness)
#####
#Count number of total votes and make sure it isn't 0
####
    print(len(s.get_account_votes(currentWitness)))
    if len(s.get_account_votes(currentWitness)) > 0:
        totalVoteslist.append(len(s.get_account_votes(currentWitness)))
#####
#Convert voting activity to csv file, 
#splitting individual post URLs into author name and title
####
        tempDf=pd.DataFrame(s.get_account_votes(currentWitness))
        tempDf["authorName"], tempDf["postName"] = zip(*tempDf["authorperm"].str.split(pat="/").tolist())
        del tempDf["authorperm"]
        tempDf.to_csv("votes_%s.csv" % currentWitness)
#####
#Count number of self votes
####
        numberSelfvotes=tempDf.authorName.value_counts()[currentWitness]
        print(numberSelfvotes)
        selfVoteslist.append(numberSelfvotes)
        
        indVotes=tempDf.groupby('authorName').authorName.count().to_frame(name = 'count')
        indVotessort=indVotes.sort_values(by='count', ascending=False)
        print(indVotessort)
        indVotessort.to_csv("indvotes_%s.csv" % currentWitness)
        
        authorNamelist=indVotes.authorName.tolist()
        repNum=[]
        print(authorNamelist)
        for author in authorNamelist:
            repNum.append(s.get_account_reputations(author,100))
        print(repNum)
        repList=[]
        for rep in repNum:
            output = int(rep[0]['reputation'])
            repReal=math.log10(output)*9 - 56
            repList.append(repReal)
        print(repList)
       
    else:
        print("account has no votes")
        selfVoteslist.append(0)
        totalVoteslist.append(0)
print(selfVoteslist)
svDF=pd.DataFrame({'Witness': witnesses, '# of SVs': selfVoteslist,'Total Votes': totalVoteslist})
svDF.to_csv('selfvoteStats.csv')




    


