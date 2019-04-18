from sklearn import preprocessing,neural_network,model_selection,datasets,cluster,externals,svm
import random
import matplotlib.pyplot as plt
import numpy as np
import os
STORESIZE = 5
SAVE_PATH = "/home/sauron/MAGI/stored_data/test/"

class Estimator:
    def __init__(self,accuracy, groupName, eps = 0.3, min_samples = 10):
        self.scaler = None
        self.groupName = groupName
        if os.access(SAVE_PATH + "model_" + groupName, os.F_OK):
            self.load_model("model_" + groupName)
        else:
            print("load fail,new a model")
            self.nn = neural_network.MLPRegressor()

        self.svm = svm.SVC(kernel='linear')
        self.accuracy_demand = accuracy
        self.curr_score = 0
        self.eps = eps
        self.min_samples = min_samples
        self.count = 0



    def find_sv_i(self, train_X, train_y):
        #print(train_X)
        #print(train_y)
        self.svm.fit(np.array(train_X),np.array(train_y))
        #print("support:")
        #print(self.svm.support_)
        return self.svm.support_


    def find_sv_statisfy_v(self, train_X, train_y, sla):
        #print("find_sv_statisy_v")
        #print(train_X)
        #print(train_y)
        res = []
        find_y = []
        true_count = False
        false_count = False
        for i in range(len(train_X)):
            if float(train_y[i]) > sla:
                find_y.append(1)
                true_count = True
            else:
                find_y.append(0)
                false_count = True
        if true_count and false_count:
            indexS = self.find_sv_i(train_X, find_y)
            for i in indexS:
                if float(train_y[i]) > sla:
                    res.append(train_X[i])
        elif true_count:# randomly select 10
            for i in range(10):
                if float(train_y[i]) > sla:
                    res.append(train_X[i])
        else:
            return -1
        return res



    def store_model(self, name):
        externals.joblib.dump(self.nn,SAVE_PATH + name)


    def load_model(self, name):
        self.nn = externals.joblib.load(SAVE_PATH + name)


    def workable(self):
        if self.accuracy_demand < self.curr_score:
            return True
        return False

    def scaler_init(self, X):
        self.scaler = preprocessing.Normalizer()
        self.scaler.fit(X)


    def pre_data(self, X, y):
        X = np.array(X)
        y = np.array(y)
        X = self.scaler.transform(X)
        if X.ndim <= 100:
            return X,y
        #Xy = np.column_stack((X,y))
        db = cluster.DBSCAN(eps=self.eps, min_samples=self.min_samples).fit(X)
        noise = []
        for i in range(len(db.labels_)):
            if db.labels_[i] == -1:
                noise.append(i)
        return np.delete(X, noise, 0), np.delete(y, noise, 0)
        #X = Xy[:, 0: - 1]
        #y = Xy[:, -1]


    def train(self,X,y):
        if X.ndim < 10:
            print("Err: No enough data for training")
            return -1
        X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, random_state=random.randint(0,10))
        self.nn.partial_fit(X_train,y_train)
        self.curr_score = self.nn.score(X_test,y_test)
        print("curr_score:" + str(self.curr_score))
        self.count += 1
        if self.count == STORESIZE:
            self.count = 0
            self.store_model("model_" + self.groupName)

        #self.curr_score = model_selection.cross_val_score(self.model,X_train,Y_train,cv=5,scoring='accuracy').mean()


    def inference(self, X):
        return float(self.nn.predict([X])[0])


if __name__ == '__main__':

    loaded_data = datasets.load_boston()
    data_x = loaded_data.data
    data_y = loaded_data.target

    ss = svm.SVC(kernel='linear')
    ss.fit(data_x,data_y)
    #nn = externals.joblib.load(SAVE_PATH + "model_sta")
    #print(data_y)
    e = Estimator(0.3,"sta")
    e.scaler_init(data_x)

    newX, newy = e.pre_data(data_x, data_y)

    for i in range(1):
        e.train(newX, newy)
        if i % 100 == 0:
            print(e.curr_score)






