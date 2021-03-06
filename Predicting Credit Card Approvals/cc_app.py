# ## 1. Credit card applications

# Import pandas
import pandas as pd

#!head -10 'datasets/cc_approvals.data'
# Load dataset
cc_apps = pd.read_csv('datasets/cc_approvals.data', sep = ',', header = None, names = ['Gender', 'Age', 'Debt', 'Married', 'BankCustomer', 'EducationLevel', 'Ethnicity', 'YearsEmployed', 'PriorDefault', 'Employed', 'CreditScore', 'DriversLicense', 'Citizen', 'ZipCode', 'Income', 'ApprovalStatus'])

# Inspect data
print(cc_apps.head())


# ## 2. Inspecting the applications

# Print summary statistics
cc_apps_description = cc_apps.describe()
print(cc_apps_description)

print("\n")

# Print DataFrame information
cc_apps_info = cc_apps.info()
print(cc_apps_info)

print("\n")

# Inspect missing values in the dataset
print(cc_apps.tail(17))


# ## 3. Handling the missing values (part i)

# Import numpy
import numpy as np

# Inspect missing values in the dataset
#cc_apps.where(cc_apps == '?') 

# Replace the '?'s with NaN
cc_apps = cc_apps.replace(to_replace = '?', value = np.nan)

# Inspect the missing values again
print(cc_apps.tail(17))


# ## 4. Handling the missing values (part ii)

# Impute the missing values with mean imputation
cols = [2, 7, 10, 14]
for i in cols:
    cc_apps.iloc[:, i].fillna(cc_apps.mean(axis = 1), inplace=True)

# Count the number of NaNs in the dataset to verify
for i in cols :
    print(i, ": \n", cc_apps.iloc[:, i].isnull().value_counts())


# ## 5. Handling the missing values (part iii)

# Iterate over each column of cc_apps
for col in cc_apps.columns:
    # Check if the column is of object type
    if cc_apps[col].dtypes == 'object':
        # Impute with the most frequent value
        cc_apps = cc_apps.fillna(cc_apps[col].value_counts().index[0])

# Count the number of NaNs in the dataset and print the counts to verify
for col in cc_apps.columns:
    print(cc_apps[col].isnull().value_counts())
 


# ## 6. Preprocessing the data (part i)

# Import LabelEncoder
from sklearn.preprocessing import LabelEncoder

# Instantiate LabelEncoder
#le = LabelEncoder()

# Iterate over all the values of each column and extract their dtypes
for col in cc_apps.columns:
    # Compare if the dtype is object
    if cc_apps[col].dtypes== "object":
    # Use LabelEncoder to do the numeric transformation
        le_col = LabelEncoder()
        le_col.fit(cc_apps[col])
        cc_apps[col] = le_col.transform(cc_apps[col])


# ## 7. Preprocessing the data (part ii)

# Import MinMaxScaler
from sklearn.preprocessing import MinMaxScaler

# Drop features 10 and 13 and convert the DataFrame to a NumPy array
cc_apps = cc_apps.drop(['DriversLicense', 'ZipCode'], axis=1)
cc_apps = cc_apps.values

# Segregate features and labels into separate variables
X,y = cc_apps[:,0: 12] , cc_apps[:,13]

# Instantiate MinMaxScaler and use it to rescale
scaler = MinMaxScaler(feature_range=(0, 1))
rescaledX = scaler.fit_transform(X)


# ## 8. Splitting the dataset into train and test sets

# Import train_test_split
from sklearn.model_selection import train_test_split

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(rescaledX,
                                y,
                                test_size= 0.33,
                                random_state= 42)


# ## 9. Fitting a logistic regression model to the train set

# Import LogisticRegression
from sklearn.linear_model import LogisticRegression 

# Instantiate a LogisticRegression classifier with default parameter values
logreg = LogisticRegression()

# Fit logreg to the train set
logreg.fit(X_train, y_train)


# ## 10. Making predictions and evaluating performance

# Import confusion_matrix
from sklearn.metrics import confusion_matrix

# Use logreg to predict instances from the test set and store it
y_pred = logreg.predict(X_test)

# Get the accuracy score of logreg model and print it
print("Accuracy of logistic regression classifier: ", logreg.score(X_test, y_test))

# Print the confusion matrix of the logreg model
print(confusion_matrix(y_test, y_pred))


# ## 11. Grid searching and making the model perform better

# Import GridSearchCV
from sklearn.model_selection import GridSearchCV

# Define the grid of values for tol and max_iter
tol = [0.01, 0.001, 0.0001]
max_iter = [100, 150, 200]

# Create a dictionary where tol and max_iter are keys and the lists of their values are corresponding values
param_grid = dict({'tol': tol, 'max_iter': max_iter})


# ## 12. Finding the best performing model

# Instantiate GridSearchCV with the required parameters
grid_model = GridSearchCV(estimator= logreg, param_grid= param_grid, cv= 5)

# Fit data to grid_model
grid_model_result = grid_model.fit(rescaledX, y)

# Summarize results
best_score, best_params = grid_model_result.best_score_, grid_model_result.best_params_
print("Best: %f using %s" % (best_score, best_params))

