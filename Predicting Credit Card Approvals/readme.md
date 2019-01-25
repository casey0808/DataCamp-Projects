
## 1. Credit card applications
<p>Commercial banks receive <em>a lot</em> of applications for credit cards. Many of them get rejected for many reasons, like high loan balances, low income levels, or too many inquiries on an individual's credit report, for example. Manually analyzing these applications is mundane, error-prone, and time-consuming (and time is money!). Luckily, this task can be automated with the power of machine learning and pretty much every commercial bank does so nowadays. In this notebook, we will build an automatic credit card approval predictor using machine learning techniques, just like the real banks do!</p>
<p>We'll use the <a href="http://archive.ics.uci.edu/ml/datasets/credit+approval">Credit Card Approval dataset</a> from the UCI Machine Learning Repository. The structure of this notebook is as follows:</p>
<ul>
<li>First, we will start off by loading and viewing the dataset.</li>
<li>We will see that the dataset has a mixture of both numerical and non-numerical features, that it contains values from different ranges, plus that it contains a number of missing entries.</li>
<li>We will have to preprocess the dataset to ensure the machine learning model we choose can make good predictions.</li>
<li>After our data is in good shape, we will do some exploratory data analysis to build our intuitions.</li>
<li>Finally, we will build a machine learning model that can predict if an individual's application for a credit card will be accepted.</li>
</ul>
<p>First, loading and viewing the dataset. We find that since this data is confidential, the contributor of the dataset has anonymized the feature names.</p>


```python
# Import pandas
import pandas as pd

#!head -10 'datasets/cc_approvals.data'
# Load dataset
cc_apps = pd.read_csv('datasets/cc_approvals.data', sep = ',', header = None, names = ['Gender', 'Age', 'Debt', 'Married', 'BankCustomer', 'EducationLevel', 'Ethnicity', 'YearsEmployed', 'PriorDefault', 'Employed', 'CreditScore', 'DriversLicense', 'Citizen', 'ZipCode', 'Income', 'ApprovalStatus'])

# Inspect data
print(cc_apps.head())
```

      Gender    Age   Debt Married BankCustomer EducationLevel Ethnicity  \
    0      b  30.83  0.000       u            g              w         v   
    1      a  58.67  4.460       u            g              q         h   
    2      a  24.50  0.500       u            g              q         h   
    3      b  27.83  1.540       u            g              w         v   
    4      b  20.17  5.625       u            g              w         v   
    
       YearsEmployed PriorDefault Employed  CreditScore DriversLicense Citizen  \
    0           1.25            t        t            1              f       g   
    1           3.04            t        t            6              f       g   
    2           1.50            t        f            0              f       g   
    3           3.75            t        t            5              t       g   
    4           1.71            t        f            0              f       s   
    
      ZipCode  Income ApprovalStatus  
    0   00202       0              +  
    1   00043     560              +  
    2   00280     824              +  
    3   00100       3              +  
    4   00120       0              +  
    

## 2. Inspecting the applications
<p>The output may appear a bit confusing at its first sight, but let's try to figure out the most important features of a credit card application. The features of this dataset have been anonymized to protect the privacy, but <a href="http://rstudio-pubs-static.s3.amazonaws.com/73039_9946de135c0a49daa7a0a9eda4a67a72.html">this blog</a> gives us a pretty good overview of the probable features. The probable features in a typical credit card application are <code>Gender</code>, <code>Age</code>, <code>Debt</code>, <code>Married</code>, <code>BankCustomer</code>, <code>EducationLevel</code>, <code>Ethnicity</code>, <code>YearsEmployed</code>, <code>PriorDefault</code>, <code>Employed</code>, <code>CreditScore</code>, <code>DriversLicense</code>, <code>Citizen</code>, <code>ZipCode</code>, <code>Income</code> and finally the <code>ApprovalStatus</code>. This gives us a pretty good starting point, and we can map these features with respect to the columns in the output.   </p>
<p>As we can see from our first glance at the data, the dataset has a mixture of numerical and non-numerical features. This can be fixed with some preprocessing, but before we do that, let's learn a bit more about the dataset a bit more to see if there are other dataset issues that need to be fixed.</p>


```python
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
```

                 Debt  YearsEmployed  CreditScore         Income
    count  690.000000     690.000000    690.00000     690.000000
    mean     4.758725       2.223406      2.40000    1017.385507
    std      4.978163       3.346513      4.86294    5210.102598
    min      0.000000       0.000000      0.00000       0.000000
    25%      1.000000       0.165000      0.00000       0.000000
    50%      2.750000       1.000000      0.00000       5.000000
    75%      7.207500       2.625000      3.00000     395.500000
    max     28.000000      28.500000     67.00000  100000.000000
    
    
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 690 entries, 0 to 689
    Data columns (total 16 columns):
    Gender            690 non-null object
    Age               690 non-null object
    Debt              690 non-null float64
    Married           690 non-null object
    BankCustomer      690 non-null object
    EducationLevel    690 non-null object
    Ethnicity         690 non-null object
    YearsEmployed     690 non-null float64
    PriorDefault      690 non-null object
    Employed          690 non-null object
    CreditScore       690 non-null int64
    DriversLicense    690 non-null object
    Citizen           690 non-null object
    ZipCode           690 non-null object
    Income            690 non-null int64
    ApprovalStatus    690 non-null object
    dtypes: float64(2), int64(2), object(12)
    memory usage: 86.3+ KB
    None
    
    
        Gender    Age    Debt Married BankCustomer EducationLevel Ethnicity  \
    673      ?  29.50   2.000       y            p              e         h   
    674      a  37.33   2.500       u            g              i         h   
    675      a  41.58   1.040       u            g             aa         v   
    676      a  30.58  10.665       u            g              q         h   
    677      b  19.42   7.250       u            g              m         v   
    678      a  17.92  10.210       u            g             ff        ff   
    679      a  20.08   1.250       u            g              c         v   
    680      b  19.50   0.290       u            g              k         v   
    681      b  27.83   1.000       y            p              d         h   
    682      b  17.08   3.290       u            g              i         v   
    683      b  36.42   0.750       y            p              d         v   
    684      b  40.58   3.290       u            g              m         v   
    685      b  21.08  10.085       y            p              e         h   
    686      a  22.67   0.750       u            g              c         v   
    687      a  25.25  13.500       y            p             ff        ff   
    688      b  17.92   0.205       u            g             aa         v   
    689      b  35.00   3.375       u            g              c         h   
    
         YearsEmployed PriorDefault Employed  CreditScore DriversLicense Citizen  \
    673          2.000            f        f            0              f       g   
    674          0.210            f        f            0              f       g   
    675          0.665            f        f            0              f       g   
    676          0.085            f        t           12              t       g   
    677          0.040            f        t            1              f       g   
    678          0.000            f        f            0              f       g   
    679          0.000            f        f            0              f       g   
    680          0.290            f        f            0              f       g   
    681          3.000            f        f            0              f       g   
    682          0.335            f        f            0              t       g   
    683          0.585            f        f            0              f       g   
    684          3.500            f        f            0              t       s   
    685          1.250            f        f            0              f       g   
    686          2.000            f        t            2              t       g   
    687          2.000            f        t            1              t       g   
    688          0.040            f        f            0              f       g   
    689          8.290            f        f            0              t       g   
    
        ZipCode  Income ApprovalStatus  
    673   00256      17              -  
    674   00260     246              -  
    675   00240     237              -  
    676   00129       3              -  
    677   00100       1              -  
    678   00000      50              -  
    679   00000       0              -  
    680   00280     364              -  
    681   00176     537              -  
    682   00140       2              -  
    683   00240       3              -  
    684   00400       0              -  
    685   00260       0              -  
    686   00200     394              -  
    687   00200       1              -  
    688   00280     750              -  
    689   00000       0              -  
    

## 3. Handling the missing values (part i)
<p>We've uncovered some issues that will affect the performance of our machine learning model(s) if they go unchanged:</p>
<ul>
<li>Our dataset contains both numeric and non-numeric data (specifically data that are of <code>float64</code>, <code>int64</code> and <code>object</code> types). Specifically, the features 2, 7, 10 and 14 contain numeric values (of types float64, float64, int64 and int64 respectively) and all the other features contain non-numeric values.</li>
<li>The dataset also contains values from several ranges. Some features have a value range of 0 - 28, some have a range of 2 - 67, and some have a range of 1017 - 100000. Apart from these, we can get useful statistical information (like <code>mean</code>, <code>max</code>, and <code>min</code>) about the features that have numerical values. </li>
<li>Finally, the dataset has missing values, which we'll take care of in this task. The missing values in the dataset are labeled with '?', which can be seen in the last cell's output.</li>
</ul>
<p>Now, let's temporarily replace these missing value question marks with NaN.</p>


```python
# Import numpy
import numpy as np

# Inspect missing values in the dataset
#cc_apps.where(cc_apps == '?') 

# Replace the '?'s with NaN
cc_apps = cc_apps.replace(to_replace = '?', value = np.nan)

# Inspect the missing values again
print(cc_apps.tail(17))
```

        Gender    Age    Debt Married BankCustomer EducationLevel Ethnicity  \
    673    NaN  29.50   2.000       y            p              e         h   
    674      a  37.33   2.500       u            g              i         h   
    675      a  41.58   1.040       u            g             aa         v   
    676      a  30.58  10.665       u            g              q         h   
    677      b  19.42   7.250       u            g              m         v   
    678      a  17.92  10.210       u            g             ff        ff   
    679      a  20.08   1.250       u            g              c         v   
    680      b  19.50   0.290       u            g              k         v   
    681      b  27.83   1.000       y            p              d         h   
    682      b  17.08   3.290       u            g              i         v   
    683      b  36.42   0.750       y            p              d         v   
    684      b  40.58   3.290       u            g              m         v   
    685      b  21.08  10.085       y            p              e         h   
    686      a  22.67   0.750       u            g              c         v   
    687      a  25.25  13.500       y            p             ff        ff   
    688      b  17.92   0.205       u            g             aa         v   
    689      b  35.00   3.375       u            g              c         h   
    
         YearsEmployed PriorDefault Employed  CreditScore DriversLicense Citizen  \
    673          2.000            f        f            0              f       g   
    674          0.210            f        f            0              f       g   
    675          0.665            f        f            0              f       g   
    676          0.085            f        t           12              t       g   
    677          0.040            f        t            1              f       g   
    678          0.000            f        f            0              f       g   
    679          0.000            f        f            0              f       g   
    680          0.290            f        f            0              f       g   
    681          3.000            f        f            0              f       g   
    682          0.335            f        f            0              t       g   
    683          0.585            f        f            0              f       g   
    684          3.500            f        f            0              t       s   
    685          1.250            f        f            0              f       g   
    686          2.000            f        t            2              t       g   
    687          2.000            f        t            1              t       g   
    688          0.040            f        f            0              f       g   
    689          8.290            f        f            0              t       g   
    
        ZipCode  Income ApprovalStatus  
    673   00256      17              -  
    674   00260     246              -  
    675   00240     237              -  
    676   00129       3              -  
    677   00100       1              -  
    678   00000      50              -  
    679   00000       0              -  
    680   00280     364              -  
    681   00176     537              -  
    682   00140       2              -  
    683   00240       3              -  
    684   00400       0              -  
    685   00260       0              -  
    686   00200     394              -  
    687   00200       1              -  
    688   00280     750              -  
    689   00000       0              -  
    

## 4. Handling the missing values (part ii)
<p>We replaced all the question marks with NaNs. This is going to help us in the next missing value treatment that we are going to perform.</p>
<p>An important question that gets raised here is <em>why are we giving so much importance to missing values</em>? Can't they be just ignored? Ignoring missing values can affect the performance of a machine learning model heavily. While ignoring the missing values our machine learning model may miss out on information about the dataset that may be useful for its training. Then, there are many models which cannot handle missing values implicitly such as LDA. </p>
<p>So, to avoid this problem, we are going to impute the missing values with a strategy called mean imputation.</p>


```python
# Impute the missing values with mean imputation
cols = [2, 7, 10, 14]
for i in cols:
    cc_apps.iloc[:, i].fillna(cc_apps.mean(axis = 1), inplace=True)

# Count the number of NaNs in the dataset to verify
for i in cols :
    print(i, ": \n", cc_apps.iloc[:, i].isnull().value_counts())

```

    2 : 
     False    690
    Name: Debt, dtype: int64
    7 : 
     False    690
    Name: YearsEmployed, dtype: int64
    10 : 
     False    690
    Name: CreditScore, dtype: int64
    14 : 
     False    690
    Name: Income, dtype: int64
    

## 5. Handling the missing values (part iii)
<p>We have successfully taken care of the missing values present in the numeric columns. There are still some missing values to be imputed for columns 0, 1, 3, 4, 5, 6 and 13. All of these columns contain non-numeric data and this why the mean imputation strategy would not work here. This needs a different treatment. </p>
<p>We are going to impute these missing values with the most frequent values as present in the respective columns. This is <a href="https://www.datacamp.com/community/tutorials/categorical-data">good practice</a> when it comes to imputing missing values for categorical data in general.</p>


```python
# Iterate over each column of cc_apps
for col in cc_apps.columns:
    # Check if the column is of object type
    if cc_apps[col].dtypes == 'object':
        # Impute with the most frequent value
        cc_apps = cc_apps.fillna(cc_apps[col].value_counts().index[0])

# Count the number of NaNs in the dataset and print the counts to verify
for col in cc_apps.columns:
    print(cc_apps[col].isnull().value_counts())
 
```

    False    690
    Name: Gender, dtype: int64
    False    690
    Name: Age, dtype: int64
    False    690
    Name: Debt, dtype: int64
    False    690
    Name: Married, dtype: int64
    False    690
    Name: BankCustomer, dtype: int64
    False    690
    Name: EducationLevel, dtype: int64
    False    690
    Name: Ethnicity, dtype: int64
    False    690
    Name: YearsEmployed, dtype: int64
    False    690
    Name: PriorDefault, dtype: int64
    False    690
    Name: Employed, dtype: int64
    False    690
    Name: CreditScore, dtype: int64
    False    690
    Name: DriversLicense, dtype: int64
    False    690
    Name: Citizen, dtype: int64
    False    690
    Name: ZipCode, dtype: int64
    False    690
    Name: Income, dtype: int64
    False    690
    Name: ApprovalStatus, dtype: int64
    

## 6. Preprocessing the data (part i)
<p>The missing values are now successfully handled.</p>
<p>There is still some minor but essential data preprocessing needed before we proceed towards building our machine learning model. We are going to divide these remaining preprocessing steps into two main tasks:</p>
<ol>
<li>Convert the non-numeric data into numeric.</li>
<li>Scale the feature values to a uniform range.</li>
</ol>
<p>First, we will be converting all the non-numeric values into numeric ones. We do this because not only it results in a faster computation but also many machine learning models (like XGBoost) (and especially the ones developed using scikit-learn) require the data to be in a strictly numeric format. We will do this by using a technique called <a href="http://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html">label encoding</a>.</p>


```python
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
```

## 7. Preprocessing the data (part ii)
<p>We have successfully converted all the non-numeric values to numeric ones. </p>
<p>Now, let's try to understand what these scaled values mean in the real world. Let's use <code>CreditScore</code> as an example. The creidt score of a person is their creditworthiness based on their credit history. The higher this number, the more financially trustworthy a person is considered to be. So, a <code>CreditScore</code> of 1 is the highest since we're rescaling all the values to the range of 0-1.</p>
<p>Also, features like <code>DriversLicense</code> and <code>ZipCode</code> are not as important as the other features in the dataset for predicting credit card approvals. We should drop them to design our machine learning model with the best set of features. This is often called feature engineering or, more specifically, feature selection.</p>


```python
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
```

## 8. Splitting the dataset into train and test sets
<p>Now that we have our data in a machine learning modeling-friendly shape, we are really ready to proceed towards creating a machine learning model to predict which credit card applications will be accepted and which will be rejected. </p>
<p>First, we will split our data into train set and test set to prepare our data for two different phases of machine learning modeling: training and testing.</p>


```python
# Import train_test_split
from sklearn.model_selection import train_test_split

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(rescaledX,
                                y,
                                test_size= 0.33,
                                random_state= 42)
```

## 9. Fitting a logistic regression model to the train set
<p>Essentially, predicting if a credit card application will be approved or not is a <a href="https://en.wikipedia.org/wiki/Statistical_classification">classification</a> task. <a href="http://archive.ics.uci.edu/ml/machine-learning-databases/credit-screening/crx.names">According to UCI</a>, our dataset contains more instances that correspond to "Denied" status than instances corresponding to "Approved" status. Specifically, out of 690 instances, there are 383 (55.5%) applications that got denied and 307 (44.5%) applications that got approved. </p>
<p>This gives us a benchmark. A good machine learning model should be able to accurately predict the status of the applications with respect to these statistics.</p>
<p>Which model should we pick? A question to ask is: <em>are the features that affect the credit card approval decision process correlated with each other?</em> Although we can measure correlation, that is outside the scope of this notebook, so we'll rely on our intuition that they indeed are correlated for now. Because of this correlation, we'll take advantage of the fact that generalized linear models perform well in these cases. Let's start our machine learning modeling with a Logistic Regression model (a generalized linear model).</p>


```python
# Import LogisticRegression
from sklearn.linear_model import LogisticRegression 

# Instantiate a LogisticRegression classifier with default parameter values
logreg = LogisticRegression()

# Fit logreg to the train set
logreg.fit(X_train, y_train)
```




    LogisticRegression(C=1.0, class_weight=None, dual=False, fit_intercept=True,
              intercept_scaling=1, max_iter=100, multi_class='ovr', n_jobs=1,
              penalty='l2', random_state=None, solver='liblinear', tol=0.0001,
              verbose=0, warm_start=False)



## 10. Making predictions and evaluating performance
<p>But how well does our model perform? </p>
<p>We will now evaluate our model on the test set with respect to <a href="https://developers.google.com/machine-learning/crash-course/classification/accuracy">classification accuracy</a>. But we will also take a look the model's <a href="http://www.dataschool.io/simple-guide-to-confusion-matrix-terminology/">confusion matrix</a>. In the case of predicting credit card applications, it is equally important to see if our machine learning model is able to predict the approval status of the applications as denied that originally got denied. If our model is not performing well in this aspect, then it might end up approving the application that should have been approved. The confusion matrix helps us to view our model's performance from these aspects.  </p>


```python
# Import confusion_matrix
from sklearn.metrics import confusion_matrix

# Use logreg to predict instances from the test set and store it
y_pred = logreg.predict(X_test)

# Get the accuracy score of logreg model and print it
print("Accuracy of logistic regression classifier: ", logreg.score(X_test, y_test))

# Print the confusion matrix of the logreg model
print(confusion_matrix(y_test, y_pred))
```

    Accuracy of logistic regression classifier:  0.837719298246
    [[92 11]
     [26 99]]
    

## 11. Grid searching and making the model perform better
<p>Our model was pretty good! It was able to yield an accuracy score of almost 84%.</p>
<p>For the confusion matrix, the first element of the of the first row of the confusion matrix denotes the true negatives meaning the number of negative instances (denied applications) predicted by the model correctly. And the last element of the second row of the confusion matrix denotes the true positives meaning the number of positive instances (approved applications) predicted by the model correctly.</p>
<p>Let's see if we can do better. We can perform a <a href="https://machinelearningmastery.com/how-to-tune-algorithm-parameters-with-scikit-learn/">grid search</a> of the model parameters to improve the model's ability to predict credit card approvals.</p>
<p><a href="http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html">scikit-learn's implementation of logistic regression</a> consists of different hyperparameters but we will grid search over the following two:</p>
<ul>
<li>tol</li>
<li>max_iter</li>
</ul>


```python
# Import GridSearchCV
from sklearn.model_selection import GridSearchCV

# Define the grid of values for tol and max_iter
tol = [0.01, 0.001, 0.0001]
max_iter = [100, 150, 200]

# Create a dictionary where tol and max_iter are keys and the lists of their values are corresponding values
param_grid = dict({'tol': tol, 'max_iter': max_iter})
```

## 12. Finding the best performing model
<p>We have defined the grid of hyperparameter values and converted them into a single dictionary format which <code>GridSearchCV()</code> expects as one of its parameters. Now, we will begin the grid search to see which values perform best.</p>
<p>We will instantiate <code>GridSearchCV()</code> with our earlier <code>logreg</code> model with all the data we have. Instead of passing train and test sets, we will supply <code>rescaledX</code> and <code>y</code>. We will also instruct <code>GridSearchCV()</code> to perform a <a href="https://www.dataschool.io/machine-learning-with-scikit-learn/">cross-validation</a> of five folds.</p>
<p>We'll end the notebook by storing the best-achieved score and the respective best parameters.</p>
<p>While building this credit card predictor, we tackled some of the most widely-known preprocessing steps such as <strong>scaling</strong>, <strong>label encoding</strong>, and <strong>missing value imputation</strong>. We finished with some <strong>machine learning</strong> to predict if a person's application for a credit card would get approved or not given some information about that person.</p>


```python
# Instantiate GridSearchCV with the required parameters
grid_model = GridSearchCV(estimator= logreg, param_grid= param_grid, cv= 5)

# Fit data to grid_model
grid_model_result = grid_model.fit(rescaledX, y)

# Summarize results
best_score, best_params = grid_model_result.best_score_, grid_model_result.best_params_
print("Best: %f using %s" % (best_score, best_params))
```

    Best: 0.852174 using {'max_iter': 100, 'tol': 0.01}
    


```python

```