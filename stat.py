#import statsmodels.formula.api as smf
import statsmodels.api as sm
import pandas
from patsy import dmatrices
import numpy as np
from scipy import stats
import pylab as pl
#from matplotlib import pyplot as plt

def main():
   
    # df = pandas.read_csv('~/Documents/4/PenteData')
    # vars = ['y','x11','x12','x13','x14','x15','x16','x21','x22','x23','x24','x25','x26']
    # df = df[vars]
    # Y,X = dmatrices('y ~ x11 + x12 + x13 + x14 + x15 + x16 +x21 + x22 + x23 + x24 + x25 + x26', data=df,return_type='dataframe')
    # mod = sm.OLS(Y,X)
    # res = mod.fit()
    # print res.params
    #print res.summary()
    #print df
    #df[-5:]
    df = pandas.read_csv('~/Documents/4/PenteData')
    vars = ['y','x11','x12','x13','x14','x15','x21','x22','x23','x24','x25']
    df = df[vars]
    #data = sm.datasets.PenteData.load()
    data = df
    #print(data)
    #data.exog = sm.add_constant(data.exog)
    Y,X = dmatrices('y ~ x11 + x12 + x13 + x14 + x15 + x21 + x22 + x23 + x24 + x25', data=df,return_type='dataframe')
    #data.exog = sm.add_constant(X, prepend=False)
    #print data.exog
    #X = sm.add_constant(X)
    logit_model = sm.GLM(Y,data.exog,family=sm.families.Binomial())
    #logit_model = smf.logit('y ~ x11 + x12 + x13 + x14 + x15 + x21 + x22 + x23 + x24 + x25', data=df)
    res = logit_model.fit()
    print(res.summary())
    #print(X)
    #print(Y)

if __name__=='__main__': main()
