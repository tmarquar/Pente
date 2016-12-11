#import statsmodels.api as sm
#import pandas
#from patsy import dmatrices
from Pente import *
#import statsmodels.formula.api as smf
import statsmodels.api as sm
import pandas as pd
from patsy import dmatrices
import numpy as np
from scipy import stats
import pylab as pl

last_white_piece_played = [None,None]
last_black_piece_played = [None,None]
white_pieces_captured = 0
black_pieces_captured = 0


def getWeights():
    df = pd.read_csv('~/Documents/4/PenteData')
    vars = ['y','x11','x12','x13','x14','x15','x21','x22','x23','x24','x25']
    df = df[vars]
    Y,X = dmatrices('y ~ x11 + x12 + x13 + x14 + x15 + x21 + x22 + x23 + x24 + x25', data=df,return_type='dataframe')
    mod = sm.OLS(Y,X)
    res = mod.fit()
    #print res.params
    return res.params

def logitWeights():
    df = pd.read_csv('~/Documents/4/PenteData')
    cols_to_keep = ['y','x12','x13','x14','x22','x23','x24']
    data = df[cols_to_keep]
    data['intercept'] = 1.0
    train_cols = data.columns[1:]
    logit = sm.Logit(data['y'],data[train_cols])   
    result = logit.fit()
    return result.params


# def getLogitWeights():
#     data = pandas.read_csv('~/Documents/4/PenteData')
#     vars = ['y','x11','x12','x13','x14','x15','x21','x22','x23','x24','x25']
#     data = data[vars]
#     data.exog = sm.add_constant(data.exog)

#     logit_model = sm.GLM(data.endog,data.exog,family=sm.families.Binomial())
#     res = logit_model.fit()
#     print(res.summary())



def getLegalActions(player,gameState):
    actions = []
    for x in range(0,17):
        for y in range(0,17):
            #print "State: ", gameState[x,y]
            #print x, ",", y
            if gameState[x,y] == 0.0:
                actions.append((x,y))

    return actions

