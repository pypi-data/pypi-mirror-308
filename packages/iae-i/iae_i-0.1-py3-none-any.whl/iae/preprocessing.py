import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import KNNImputer

def basic(df):
#     import pandas as pd
    # import numpy as np
    # import matplotlib.pyplot as plt
    # from sklearn.model_selection import train_test_split
    # from sklearn.decomposition import PCA
    # from sklearn.preprocessing import StandardScaler
    # from sklearn.feature_selection import SelectKBest, f_regression
    # from sklearn.metrics import mean_squared_error, r2_score
    # import tensorflow as tf
    # from tensorflow.keras.models import Sequential
    # from tensorflow.keras.layers import Dense
    # from sklearn.impute import KNNImputer
    df.info()
    df.isnull().sum()
    df = df.dropna(subset=['Price'])
    df_temp = df[['Bedroom2', 'Bathroom', 'Car', 'Landsize', 'BuildingArea', 'YearBuilt']]
    df_temp.describe()

    df_temp.boxplot(figsize=(10, 5))
    # plt.show()

    # Plotting the distributions for columns with missing values which we want to impute

    # histogram for Bedroom2
    # plt.figure(figsize=(10, 6))
    # df['Bedroom2'].plot(kind='hist', bins=50)
    # plt.title('Bedroom2 distribution')
    # plt.show()

    # # histogram for Bathroom
    # plt.figure(figsize=(10, 6))
    # df['Bathroom'].plot(kind='hist', bins=50)
    # plt.title('Bathroom distribution')
    # plt.show()

    # # histogram for Car
    # plt.figure(figsize=(10, 6))
    # df['Car'].plot(kind='hist', bins=50)
    # plt.title('Car distribution')
    # plt.show()

    # # Line plot for Landsize
    # plt.figure(figsize=(10, 6))
    # df['Landsize'].plot(kind='line')    
    # plt.title('Landsize distribution')
    # plt.show()

    # # Line plot for BuildingArea
    # plt.figure(figsize=(10, 6))
    # df['BuildingArea'].plot(kind='line')
    # plt.title('BuildingArea distribution')
    # plt.show()

    # # histogram for YearBuilt
    # plt.figure(figsize=(10, 6))
    # df['YearBuilt'].plot(kind='hist', bins=50)
    # plt.title('YearBuilt distribution')
    # plt.show()
        

def missing_values(df):
    # mean when distribution is normal
    # median when distribution is skwed
    # mode when categorical


    # Impute missing values
    df['Bedroom2'] = df.groupby(['Suburb', 'Rooms'])['Bedroom2'].transform(
        lambda x: x.fillna(x.mode().iloc[0]) if not x.mode().empty and x.notnull().any() else x)

    df['Bathroom'] = df.groupby(['Suburb', 'Rooms'])['Bathroom'].transform(
        lambda x: x.fillna(x.mode().iloc[0]) if not x.mode().empty and x.notnull().any() else x)

    df['Car'] = df.groupby(['Suburb', 'Rooms'])['Car'].transform(
        lambda x: x.fillna(x.mode().iloc[0]) if not x.mode().empty and x.notnull().any() else x)

    df['YearBuilt'] = df.groupby(['Suburb', 'Rooms'])['YearBuilt'].transform(
        lambda x: x.fillna(x.median()) if x.notnull().any() else x)




    imputer = KNNImputer(n_neighbors=5)
    df['Landsize'] = imputer.fit_transform(df[['Landsize']])
    df['BuildingArea'] = imputer.fit_transform(df[['BuildingArea']])

def one_hot(df):
    df = pd.get_dummies(df, columns=['Type', 'Method', 'Regionname','Suburb','CouncilArea'])


def scaling(df):
    # X_complex = df_complex.drop('Price', axis=1)
    # y = df_complex['Price']

    # Scale target variable (y) using MinMaxScaler
    # from sklearn.preprocessing import MinMaxScaler
    y_scaler = MinMaxScaler()
    y = y_scaler.fit_transform(y.values.reshape(-1, 1))

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_complex)

def correlation(df):
    correlation_matirx = df_complex.corr()
    target_correlation = correlation_matirx['Price'].abs()


def split(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X,y,random_state=42,test_size=0.2)
    