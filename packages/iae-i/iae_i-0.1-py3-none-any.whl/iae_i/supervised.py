
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

from sklearn.model_selection import train_test_split

def correlation(df_temp):
    correlation_matirx = df_temp.corr()
    target_correlation = correlation_matirx['Price'].abs()
    selected_features = target_correlation[target_correlation > 0.1].index
    X = df_temp[selected_features]
    X.drop('Price', axis=1, inplace=True)
    X.fillna(0, inplace=True)
    y = df_temp['Price']

def linear_r(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    linear = LinearRegression()
    linear.fit(X_train, y_train)

    # Predicting the Test set results
    y_pred = linear.predict(X_test)

    print('Mean Squared Error:', mean_squared_error(y_test, y_pred))
    print('Mean Absolute Error:', mean_absolute_error(y_test, y_pred))
    print('R^2:', r2_score(y_test, y_pred))

    # accuracy
    print(linear.score(X_test, y_test))

    logistic = LogisticRegression()
    logistic.fit(X_train, y_train)


    print(logistic.score(X_test,y_test))