# Regression for classification using lasso and Enet
# Based on http://scikit-learn.org/stable/auto_examples/linear_model/plot_lasso_and_elasticnet.html
#
# The target values are taken from https://info.worldbank.org/governance/wgi/pdf/prs.xlsx
# Canary 2018
from __future__ import print_function
import pandas as pd
import numpy as np
from models import Data, Risk, Country
from django.conf import settings
from django.db.models import Avg
from datetime import datetime

from sklearn.linear_model import Lasso
from sklearn.metrics import r2_score

class RiskClassifier():
    def __init__(self, train = False):
        if train:
            self.train()
        #else:
            #Load classifier

    def train(self, plot = False):
        X, y = self.get_database_train_data()
        
        n_samples = X.shape[0]
        X_train, y_train = X[:n_samples // 2], y[:n_samples // 2]
        X_test, y_test = X[n_samples // 2:], y[n_samples // 2:]
        #######################################################################
        # Lasso
        alpha = 0.1
        self.lasso = Lasso(alpha=alpha)

        y_pred_lasso = self.lasso.fit(X_train, y_train).predict(X_test)
        r2_score_lasso = r2_score(y_test, y_pred_lasso)
        print(self.lasso)
        print("r^2 on test data : %f" % r2_score_lasso)
        # #####################################################################
        # ElasticNet
        from sklearn.linear_model import ElasticNet

        self.enet = ElasticNet(alpha=alpha, l1_ratio=0.7)

        y_pred_enet = self.enet.fit(X_train, y_train).predict(X_test)
        r2_score_enet = r2_score(y_test, y_pred_enet)
        print(self.enet)
        print("r^2 on test data : %f" % r2_score_enet)
        if plot:
            import matplotlib.pyplot as plt
            plt.plot(self.enet.coef_, color='lightgreen', linewidth=2, \
             label='Elastic net coefficients')
            plt.plot(self.lasso.coef_, color='gold', linewidth=2, \
                     label='Lasso coefficients')
            plt.legend(loc='best')
            plt.title("Lasso R^2: %f, Elastic Net R^2: %f"
                      % (r2_score_lasso, r2_score_enet))
            plt.show()


    def classify(self, example, test = None):
        print( example )
        #perform the classification
        y_pred_lasso = self.lasso.predict(example)
        y_pred_enet = self.enet.predict(example)
        if not test is None:
            r2_score_lasso = r2_score(test, y_pred_lasso)
            r2_score_enet = r2_score(test, y_pred_enet)
            print("r^2 Classify Lasso test: %f" % r2_score_lasso)
            print("r^2 Classify Enet test: %f" % r2_score_enet)
        
        return y_pred_lasso, y_pred_enet
    
    def get_data(self, countries):
        this_year = datetime.now().year
        
        aggregates = {}
        
        data_fields = Data.objects.filter().order_by("index").values_list("index__name",flat=True).distinct()
        
        for d in data_fields:
            aggregates[d] = {}
            for c in countries:
                aggregate =  Data.objects.filter( country__name=c, index__name=d, year__gte=this_year-settings.PAST_YEARS ).aggregate(Avg("value"))["value__avg"]
                if aggregate is None:
                    aggregate =  Data.objects.filter( country__name=c, index__name=d ).aggregate(Avg("value"))["value__avg"]
                    if aggregate is None:
                        aggregate = Data.objects.filter( index__name=d ).aggregate(Avg("value"))["value__avg"]
                aggregates[d][c] = aggregate
        
        database_data = { k: [] for k in data_fields }
        
        for c in countries:
            for d in data_fields:
                database_data[d].append(aggregates[d][c])
        return database_data

    def get_database_to_classify_data(self):
        risks = Risk.objects.all()
        countries = list( set( map( lambda r: r.country.name, risks ) ) )
        countries = Country.objects.exclude(name__in=countries).values_list('name', flat=True)
        database_data = self.get_data(countries)

        data_fields = Data.objects.filter().order_by("index__name").values_list("index__name",flat=True).distinct()
        
        df = pd.DataFrame( database_data )
        return df[list(data_fields)], countries

    def get_database_train_data(self):
        
        risks = Risk.objects.all()
        countries = list( set( map( lambda r: r.country.name, risks ) ) )
        database_data = self.get_data(countries)
        num_risks = {}
        
        # Convert the risks to numbers.
        for c in countries:
            nr = map( lambda v: 1.0 if v == 'HIGH' else 0.5, risks.filter( country__name=c ).values_list('value', flat=True) )
            num_risks[c] = ( nr[0] + nr[1] )/2.0
        
        aggregates = {}
        
        data_fields = Data.objects.filter().order_by("index__name").values_list("index__name",flat=True).distinct()
        
        database_data["Risk"] = []
        
        for c in countries:
            database_data["Risk"].append(num_risks[c])
        
        df = pd.DataFrame( database_data )
        
        return df[list(data_fields)], df["Risk"]

    def getAllData(self):
        dfCorruption = pd.read_csv('../economy/Corruption.csv',sep=';', na_values=0)
        dfEducation = pd.read_csv('../economy/Education.csv',sep=';', na_values=0)
        dfGini = pd.read_csv('../economy/Gini.csv',sep=';', na_values=0)
        dfImports = pd.read_csv('../economy/Imports.csv',sep=';', na_values=0)
        dfInflation = pd.read_csv('../economy/Inflation.csv',sep=';', na_values=0)
        dfPopulation = pd.read_csv('../economy/Population.csv',sep=';', na_values=0)
        dfReserves = pd.read_csv('../economy/Reserves.csv',sep=';', na_values=0)
        dfUnemployment = pd.read_csv('../economy/Unemployment.csv',sep=';', na_values=0)

        riskData = pd.read_csv('../targets/psr.csv', na_values=0)

        # result = pd.concat([dfCorruption, dfEducation, dfGini, dfImports, dfInflation, dfPopulation, dfReserves, dfUnemployment], axis=1, join='inner')
        allData = dfCorruption.set_index('Country Name') \
                .join(dfEducation.set_index('Country Name'), lsuffix='_corruption') \
                .join(dfGini.set_index('Country Name'), lsuffix='_education') \
                .join(dfImports.set_index('Country Name'),lsuffix='_gini') \
                .join(dfInflation.set_index('Country Name'),lsuffix='_imports') \
                .join(dfPopulation.set_index('Country Name'), lsuffix = '_inflation') \
                .join(dfReserves.set_index('Country Name'), lsuffix = '_population') \
                .join(dfUnemployment.set_index('Country Name'), lsuffix = '_reserves', rsuffix = '_unemployment')

        allData = allData.join(riskData.set_index('Country Name'), how='inner')
        return allData

    def getDataFromYear(self, year):
        allData = self.getAllData()
        strYear = str(year)

        data = allData[[strYear+'_corruption',strYear+'_education',strYear+'_gini',strYear+'_imports',strYear+'_inflation',strYear+'_population',strYear+'_reserves',strYear+'_unemployment']].fillna(0)

        risk = allData[[strYear+'_PRS'+strYear[2:]+'VA', \
                strYear+'_PRS'+strYear[2:]+'PV', \
                strYear+'_PRS'+strYear[2:]+'GE', \
                strYear+'_PRS'+strYear[2:]+'RQ', \
                strYear+'_PRS'+strYear[2:]+'RL', \
                strYear+'_PRS'+strYear[2:]+'CC']].fillna(0)
        
        return data, risk

    def prepareData(self):
        # Someday we will have more data so we'll load more years
        # into our classifier
        data2016, risk2016 = self.getDataFromYear(2016)
        X = data2016.as_matrix()
        y = risk2016['2016_PRS16PV'].as_matrix()
        return X, y


if __name__ == "__main__":
    riskClassifier = RiskClassifier(train=True)
    data2015, risk2015 = riskClassifier.getDataFromYear(2015)
    X = data2015.as_matrix()
    y = risk2015['2015_PRS15PV'].as_matrix()
    classification_lasso, classification_enet = riskClassifier.classify(X,y)
    print (classification_lasso, classification_enet)
