import pandas as pd
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import IsolationForest
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder



from sklearn.metrics import accuracy_score, r2_score
def anamoly(df_temp):
    dbscan = DBSCAN(eps=0.5,min_samples=5)
    dbscan_labels = dbscan.fit_predict(df_temp)

    iso_foreset = IsolationForest(contamination=0.1)
    iso_labels = iso_foreset.fit_predict(df_temp)

    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.scatter(df_temp['Longtitude'], df_temp['Lattitude'], c=dbscan_labels, cmap='viridis')
    plt.title('DBSCAN Anomaly Detection')


    # Plotting Isolation Forest results
    plt.subplot(1, 2, 2)
    plt.scatter(df_temp['Longtitude'], df_temp['Lattitude'], c=iso_labels, cmap='coolwarm')
    plt.title('Isolation Forest Anomaly Detection')


    plt.tight_layout()
    plt.show()


def pca(X,y):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    pca = PCA(n_components=0.95)
    X_pca = pca.fit_transform(X_scaled)

    print("features before pca" , X.shape[1])

    X_train, X_test, y_train, y_test = train_test_split(X_pca, y, test_size=0.2, random_state=42)

    rf = RandomForestClassifier(random_state=42)
    rf.fit(X_train, y_train)

    y_pred = rf.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    print("Model Accuracy after PCA:", accuracy)
    print("Explained Variance Ratio:", pca.explained_variance_ratio_)
    print("Number of components after PCA:", pca.n_components_)


def kmeans_clustering(X,df_temp):

    kmeans = KMeans(n_clusters=10, random_state=42)
    kmeans.fit(X)

    df_temp['cluster_labels'] = kmeans.labels_

def elbow(X):

    cluster_range = range(1, 21)
    inertia = []

    for k in cluster_range:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(X)
        inertia.append(kmeans.inertia_)

    plt.figure(figsize=(10, 6))
    plt.plot(cluster_range, inertia, marker='o')
    plt.xlabel("Number of Clusters")
    plt.ylabel("Inertia")
    plt.title("Elbow Method for Optimal Clusters")
    plt.show()

def tree_threshold(X,y,df_temp):
    
    rf = RandomForestClassifier(random_state=42)

    scores = cross_val_score(rf, X, y, cv=5, scoring='accuracy')
    rf.fit(X,y)
    importance_threshold = 0.025
    important_features = X.columns[rf.feature_importances_ > importance_threshold]
    X_important = X[important_features]

    scaler = StandardScaler()
    X_important_scaled = scaler.fit_transform(X_important)

    kmeans = KMeans(n_clusters=10, random_state=42)
    kmeans.fit(X_important_scaled)

    df_temp['cluster_labels'] = kmeans.labels_


def tree_importance(X,y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


    clf = DecisionTreeClassifier()
    clf.fit(X_train,y_train)

    print(clf.score(X_test,y_test))

    rf = RandomForestClassifier()
    rf.fit(X_train,y_train)

    print(rf.score(X_test,y_test))

    plt.figure(figsize=(10,6))
    plt.barh(X.columns,clf.feature_importances_)
    plt.show()

def tree_helper(df_temp):
    df_temp['target_category'] = pd.qcut(df_temp['Price'],q=3,labels = ['Low','Medium','High'])

    le = LabelEncoder()
    df_temp['target_category_encoded'] = le.fit_transform(df_temp['target_category'])