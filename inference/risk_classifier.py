from __future__ import print_function
import pandas as pd
import numpy as np

class RiskClassifier():
    def __init__(self):
        #something to initialize it
        print ("Initialized")

    def train(self, data):
        #perform the training
        print ("Training")

    def classify(self, example):
        #perform the classification
        print ("Classifying")

    def prepareData(self):
        dfCorruption = pd.read_csv('../economy/Corruption.csv',sep=';', na_values=0)
        dfEducation = pd.read_csv('../economy/Education.csv',sep=';', na_values=0)
        dfGini = pd.read_csv('../economy/Gini.csv',sep=';', na_values=0)
        dfImports = pd.read_csv('../economy/Imports.csv',sep=';', na_values=0)
        dfInflation = pd.read_csv('../economy/Inflation.csv',sep=';', na_values=0)
        dfPopulation = pd.read_csv('../economy/Inflation.csv',sep=';', na_values=0)
        dfReserves = pd.read_csv('../economy/Reserves.csv',sep=';', na_values=0)
        dfUnemployment = pd.read_csv('../economy/Unemployment.csv',sep=';', na_values=0)
        # result = pd.concat([dfCorruption, dfEducation, dfGini, dfImports, dfInflation, dfPopulation, dfReserves, dfUnemployment], axis=1, join='inner')
        result = dfCorruption.set_index('Country Name') \
                .join(dfEducation.set_index('Country Name'),lsuffix='_corruption') \
                .join(dfGini.set_index('Country Name'), lsuffix='_education') \
                .join(dfImports.set_index('Country Name'),lsuffix='_gini') \
                .join(dfInflation.set_index('Country Name'),lsuffix='_imports') \
                .join(dfPopulation.set_index('Country Name'), lsuffix = '_inflation') \
                .join(dfReserves.set_index('Country Name'), lsuffix = '_population') \
                .join(dfUnemployment.set_index('Country Name'), lsuffix = '_reserves', rsuffix = '_unemployment')

        data2016 = result[['2016_corruption','2016_education','2016_gini','2016_imports','2016_inflation','2016_population','2016_reserves','2016_unemployment']].fillna(0)

        numpyMatrix = data2016.as_matrix()
        print(numpyMatrix.shape)

if __name__ == "__main__":
    riskClassifier = RiskClassifier()
    riskClassifier.prepareData()
