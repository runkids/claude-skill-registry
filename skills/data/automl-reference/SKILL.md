# AutoML Reference

Note:

This guide covers the low-level details on AutoML. For information about using AutoML as your provider in IntegratedML, see the IntegratedML User Guide.

AutoML is an automated machine learning system developed by InterSystems, housed within InterSystems IRIS® data platform. It is designed to quickly build accurate predictive models using your data, automating several key components
of the machine learning process:

Figure 1–1:The Machine Learning Process

Figure 1–2: Automating the Machine Learning Process

After you train your model with AutoML, you can easily deploy your model by using the SQL syntax provided by IntegratedML.

Highlighted Features of AutoML

This section describes some of the machine learning features used by AutoML to smartly produce predictive models.

### 2.1 Natural Language Processing

AutoML leverages natural language processing (NLP) to turn your text features into numeric features for your predictive models. AutoML uses Term frequency-inverse document frequency (TFIDF) to evaluate key words in text and list columns.

### 2.2 Multi-Hot Encoding

While most of our data is sparse, machine learning algorithms can only understand dense data. In most data modeling workflo ws, data scientists are burdened with performing difficult, and cumbersome, manual transformations to con vert their sparse data into dense data.

Unlike many workflo ws that require this manual step, AutoML performs this conversion seamlessly. Lists and one-to-many relationships are smartly “multi-hot encoded” to account for columns that are representing more than a single value.

For instance, assume a table that contains a list of medical conditions for each person:

Person

Person A

Person B

Person C

Person D

Conditions

[‘diabetes’, ‘osteoporosis’, ‘asthma’]

[‘osteoporosis’, ‘hypertension’]

[‘asthma’, ‘hypertension’]

[‘hypertension’, ‘asthma’]

Many machine learning functions treat these lists as separate entities, with one-hot encoding resulting in the following
conversion:

Highlighted Features of AutoML

Person

[‘diabetes’, ‘osteoporosis’,‘asthma’]

[‘osteoporosis’, ‘hypertension’]

[‘asthma’, ‘hypertension’]

[‘hypertension’, ‘asthma’]

Person
A

Person
B

Person
C

Person
D

Instead, AutoML uses bag-of-words to create a separate column for each value in each list:

Person

‘diabetes’

‘osteoporosis’

‘asthma’

‘hypertension’

Person
A

Person
B

Person
C

Person
D

While other functions would have treated each person as having a separate list of medical conditions, AutoML’s method allows a model to properly find patterns between each of these persons’ set of medical conditions.

AutoML assumes that order does not matter. Person C and Person D share the same set of medical conditions, but just ordered differently. While other functions treat those two lists differently, AutoML identifies that the y are the same.

AutoML performs two key steps of feature engineering:

- Column Type Classification

- These steps help make the data compatible with the utilized machine learning algorithms, and can greatly improve performance.

### 3.1 Column Type Classification

AutoML first e xamines the columns in the dataset and classifies them as a particular Python data type. F or information about the conversion from DDL to Python data types, see DDL to Python Type Conversion.

The column types, along with how their classifications are made, are listed belo w:

Numeric Columns

Numeric columns are those that have the numeric pandas datatype, such as int8, int64, float32 , etc. All columns
meeting this condition are included, except:

- Ignored Columns.

- Columns of the timedelta datatype.

- Columns with only one unique value.

Some columns with seemingly numeric data may be inappropriately classified as numeric columns. F or example, if had a column with ID numbers for different items, an ID number of 1000 is not “half of ” an ID number of
2000. You can properly treat these columns as category columns by recasting the numeric data with VARCHAR
values.

Category Columns

Category columns are those that contain categorical values, meaning there are a relatively small, fix ed number of
values that appear. They satisfy the following criteria:

- Must be of category or object pandas datatype.

- Must not include List Columns.

- The number of unique values is less than 10% the total number of values.

Text Columns

Text columns are columns where the values look like sentences. AutoML looks for values that contain 4 or more
words. They satisfy the following criteria:

- Must be of the category or object pandas datatype.

- Must not include Category Columns.

- Must not include List Columns.

- The number of unique values is less than 10% the total number of values.

List Columns

List columns are those that contain list values. They satisfy the following criteria:

- Must be of category or object pandas datatype.

- Must be, or contain, one of the following types:

–

–

–

–

InterSystems IRIS data type %Library.String:list

InterSystems IRIS data type %Library.String:array

Python list. This is determined by checking the first 10 non-empty v alues of the column to see if the type of each value is a Python list.

String array. This is determined by checking the first 10 non-empty v alues of the column to see if the type of each value is a string, with starting character [, ending character ], and of length at least 2.

Boolean Columns

Boolean columns are those that have the bool pandas datatype. They additionally satisfy the condition that they do not include Ignored Columns.

Ignored Columns

Ignored columns are those that are to be disregarded and removed before training. These include:

- The ID column.

- The label column.

- Columns with only one unique value (except for columns of datetime pandas datatype).

Date/Time Columns

Date/Time columns are those that have the datetime pandas datatype. They additionally satisfy the condition that they do not include Ignored Columns.

See below for discussion of additional date/time columns created.

#### 3.1.1 DDL to Python Type Conversion

The following table maps DDL data types to the Python data types that AutoML uses to classify data columns.

DDL Data Type

Python Data Type

BIGINT

BINARY

BIT

DATE

DECIMAL

DOUBLE

INTEGER

NUMERIC

REAL

SMALLINT

TIME

TIMESTAMP

TINYINT

VARBINARY

VARCHAR

integer

bytes

Boolean

datetime64 (numpy)

decimal

float

integer

float

float

integer

datetime64 (numpy)

datetime64 (numpy)

integer

bytes

string

For information about DDL data types, and their associated InterSystems IRIS® data platform data types, see “Data Types” in the InterSystems SQL Reference.

### 3.2 Data Transformation

The Transform Function transforms the entire dataset into the form to be used by the machine learning models. It is applied on the training set before training, and on any future datasets before predictions are made.

Adding Additional Columns

Additional Date/Time columns are created. For every datetime column, the following separate columns are added whenever
applicable:

- Hour of day.

- Day of week.

- Month of year.

AutoML also creates duration columns. Each column added represents one of the original date/time columns, and each value in this column is the duration between the dates of that particular date/time column and all other date/time columns.
For example, consider patient data that has three date/time columns:

- Date of birth.

- Time of admission.

- Time of exit.

AutoML creates two useful duration columns from these columns: age (duration between date of birth and time of admission) and length of stay (duration between time of admission and exit).

Finally, for each list column present, another column is added simply with the size of the lists. That is, each value in the new column is the length of the corresponding list in the old column.

Replacing Missing Values

Datasets can often be incomplete, with missing values in some of their columns. To help compensate for this and improve
performance, AutoML fills in missing/NULL v alues:

- For categorical and date columns, AutoML replaces missing values with the mode (most popular value) of the column.

- For numeric and duration columns, AutoML replaces missing values with the mean (average) of the column.

- For list and text columns, AutoML replaces missing values with an empty string.

Transforming Numeric Columns

For each numeric column, a standard scalar is fit. These include the original numeric columns, along with the duration and list size columns as well.

Numerical column values are also binned and then used as categorical values. These new categorical bin columns are added on separately in addition to the already present numerical columns. Each numerical column is separated into four bins, each representing a quartile of the values in that column. The new binned columns are treated as categorical columns.

Transforming Text and List Columns

For each text and list column, a vectorizer is fit to transform the data to the appropriate form needed for training. This is done with SciKit Learn’s TFIDF Vectorizer. Please see their documentation.

The following parameters are used:

Parameter

Convert to lowercase

Stop Words

N-Gram Range

Max Features

Norm

Binary Columns

Value

True

None

(1,1)

10000

L2

Binary columns are simply transformed to be composed of 1’s and 0’s, with true values mapping to 1’s.

Categorical Columns

Categorical columns are one-hot encoded before being used for training.

Feature Elimination

As the last step before training, feature elimination is performed to remove redundancy, improve training speed, and improve the accuracy of models. This is done using Scikit Learn’s SelectFPR function.

The following parameters are used:

Parameter

Scoring function

alpha

Value

f_classif

0.2

Algorithms Used

AutoML uses four different models to make predictions.

For regression models:

- XGBRegressor

For classification models:

- Neural Network

- Logistic Regression

- 4.1 XGBRegressor For regression models, AutoML uses XGBoost’s XGBRegressor class.

The model hyperparameters are detailed below:

Hyperparameter

Max Depth

Learning Rate

Number of Estimators

Objective

Booster

Tree Method

Gamma (min loss reduction for partition on leaf)

Min Child Weight

Max Delta Step

L2 Regularization Lambda

Value

0.1

Squared Error

Gbtree

Auto

Algorithms Used

Hyperparameter

Scale Positive Weight

Base/Initial Score

### 4.2 Neural Network

Value

0.5

For the Neural Network model, AutoML uses TensorFlow with Keras as a wrapper.

The input layer has its size based on the number of features. This layer is then densely connected to a single hidden layer composed of 100 neurons, which implement the ReLU Activation Function. This hidden layer is densely connected to the final output layer , which implements the Softmax Activation Function. The number of neurons in the output layer is equivalent to the number of classes present for classification.

The model hyperparameters are detailed below:

Hyperparameter

Optimizer (name)

Beta_1

Beta_2

Epsilon

Amsgrad

Loss

Value

Adam

0.9

0.999

1e-07

False

Sparse Categorical Crossentropy

### 4.3 Logistic Regression

For the Logistic Regression Model, AutoML uses SciKit Learn’s Logistic Regression class.

The model hyperparameters are detailed below:

Hyperparameter

Penalty

Dual Formulation

Tolerance

C (Inverse Regularization Parameter)

Fit Intercept

Intercept Scaling

Class Weight

Solver

Max Iterations

Value

L2

False

1e-4

True

Balanced

liblinear

Hyperparameter

Multiclass

Warm Start

Value

One-vs-Rest

False

### 4.4 Random Forest Classifier

For the Random Forest Classifier model, AutoML uses SciKit Learn’s Random Forest Classifier class.

The model hyperparameters are detailed below:

Hyperparameter

Number of Estimators

Criterion

Max Depth

Min Samples to Split

Min Samples to be Leaf Node

Min Fraction of Total Sum of Weights to be Leaf

Max Features

Max Leaf Nodes

Min Impurity Decrease for Split

Bootstrap

Warn Start

Class Weight

Value

Gini Impurity

None

Square root of number of features

None

True

False

Balanced

Model Selection Process

If the label column is of type float or comple x, AutoML trains a regression model using XGBRegressor.

For classification models, AutoML uses the following selection process to determine the most accurate model:

1.

If the dataset is too large, AutoML samples down the data to speed up the model selection process. The full dataset is still used for training after model selection.

The size of the dataset is calculated by multiplying the number of columns by the number of rows. If this calculated size is larger than the target size, sampling is needed. The number of rows that can be utilized is calculated by dividing the target size by the number of columns. This number of rows is randomly selected from the entire dataset to be used only for the purposes of model selection.

2. AutoML determines if the dataset presents a binary classification problem, or if multiple classes are present.

- If it is a binary classification problem, the R OC AUC scoring metric is used.

- Otherwise, the F1 scoring metric is used.

3. These scoring metrics are then computed for each model using Monte Carlo cross validation, with three training/testing

splits of 70%/30%. Depending on the training mode, the best model is determined as follows:

Note:

For the mathematical expressions listed below, model_score represents the scoring metric from step 2, while model_time is the time spent training the model.

Training Mode

Expression for Model Comparison

TIME

BALANCE

SCORE

(model_score)/(model_time^1.2)

(model_score)/(model_time)

model_score

For example, if the following three models were being compared:

Model

Model A

Model B

Model C

model_score

model_time

0.7

0.85

0˙.87

In the TIME training mode, Model A would be selected.

Model Selection Process

In the BALANCE training mode, Model B would be selected.

In the SCORE training mode, Model C would be selected.
