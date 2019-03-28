from sklearn import preprocessing,neural_network,model_selection,datasets,cluster,externals
import random
import matplotlib.pyplot as plt
import numpy as np

class Estimator:
    def __init__(self,accuracy, eps = 0.3, min_samples = 10):
        self.scaler = preprocessing.Normalizer()
        self.model = neural_network.MLPRegressor()
        self.accuracy_demand = accuracy
        self.curr_score = 0
        self.eps = eps
        self.min_samples = min_samples

    def store_model(self, path = './model'):
        externals.joblib.dump(self.model,path)

    def load_model(self, path = './model'):
        self.model = externals.joblib.load(path)


    def workable(self):
        if self.accuracy_demand < self.curr_score:
            return True
        return False

    def pre_data(self, X, y):
        self.scaler.fit(X)
        X = self.scaler.transform(X)
        print(X.shape)
        #Xy = np.column_stack((X,y))
        db = cluster.DBSCAN(eps=self.eps, min_samples=self.min_samples).fit(X)
        noise = []
        for i in range(len(db.labels_)):
            if db.labels_[i] == -1:
                noise.append(i)
        X = np.delete(X, noise, 0)
        y = np.delete(y, noise, 0)
        print(X.shape)
        print(y.shape)
        #X = Xy[:, 0:Xy.shape[1] - 1]
        #y = Xy[:, Xy.shape[1]-1]
        return X,y

    def train(self,X,y):

        X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, random_state=random.randint(0,10))
        self.model.partial_fit(X_train,y_train)
        self.curr_score = self.model.score(X_test,y_test)
        #self.curr_score = model_selection.cross_val_score(self.model,X_train,Y_train,cv=5,scoring='accuracy').mean()

if __name__ == '__main__':
    loaded_data = datasets.load_boston()
    data_x = loaded_data.data
    data_y = loaded_data.target
    e = Estimator(0.3)

    newX, newy = e.pre_data(data_x, data_y)

    for i in range(100):
        e.train(newX, newy)
        if i % 100 == 0:
            print(e.curr_score)

    e.store_model()
    e.load_model()





