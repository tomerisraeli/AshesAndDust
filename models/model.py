import os
import numpy as np
import pandas as pd
import xarray as xr
import pickle
import matplotlib.pyplot as plt
from random import *
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

file_path = './h20v05_AOT_one_year.nc'
model_path = './model.sav'

def get_data(file_path):
    dataset = xr.open_dataset(file_path)
    df = dataset.to_dataframe()
    df = df.reset_index()
    return [df.dropna(),df-df.dropna()]

def split_data(data, precentage, data_type):
    data = data.drop('time', axis=1)
    X_train, X_test, y_train, y_test = train_test_split(data, data[data_type], test_size=precentage)
    return X_train, X_test, y_train, y_test

def reset_model():
    pickle.dump(None, open(model_path, 'wb'))

def save_model(rf, model_path):
    pickle.dump(rf, open(model_path, 'wb'))

def load_model(model_path):
    try:
        rf = pickle.load(open(model_path, 'rb'))
        return rf
    except:
        return RandomForestRegressor(n_estimators=10, max_depth=2) 

def train_model(df, rf):  
    X_train, X_test, y_train, y_test = split_data(df, uniform(0.15, 0.85), 'AOT')    
    rf.fit(X_train, y_train)
    y_pred = rf.predict(X_test)
    accuracy = r2_score(y_test, y_pred)    

    return [accuracy, rf]

def display_testing(num, df):
    accuracy = []
    loop = []
    rf = load_model(model_path)
    for i in range(num):
        acc,trained_rf = train_model(df, rf)
        print(acc)
        accuracy.append(acc)
        loop.append(i+1)
        rf = trained_rf

    plt.plot(loop, accuracy, linewidth = 0, marker = 'o', markerfacecolor='blue', markersize=7)
    plt.xlabel('time')
    plt.ylabel('accuracy')
    plt.title('model accuracy')

    plt.show()

    return rf

if __name__ == '__main__':
    df, complete_df = get_data(file_path)
    rf = display_testing(5, df)
    save_model(rf, model_path)


