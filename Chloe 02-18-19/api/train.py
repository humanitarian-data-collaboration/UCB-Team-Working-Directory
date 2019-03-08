import pandas as pd
import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn import linear_model



#creat some dummy data to test the api
X, y = np.arange(10).reshape((5, 2)), range(5)


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

#creating a model and training it
regr = linear_model.RidgeCV(alphas= np.arange(0.1,10.0,.5))
regr.fit(X_train, y_train)

#exporting my model
pickle.dump(regr,open("model.pkl","wb"))

# #checking for error
# ans = regr.predict(X_test)
# print mean_squared_error(y_test, ans)
