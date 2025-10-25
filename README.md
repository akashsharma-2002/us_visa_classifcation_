# us_visa_classifcation_

step 1: create template.py and run it

step2: creating virtual env

conda create -n visa python=3.8 -y

conda env list

conda activate visa


Pipelines flow:
1: creating constant 
2: creatinf artifacts folder
3: creating mongodb connection file
4: creating data acess dir where data will be converted to pandas from dictionary coming from mongo db


now start with actual flow

1️⃣ Data Ingestion

What happens:
You collect and load raw data from various sources — like databases, CSV files, APIs, sensors, or cloud storage — into your ML pipeline.
Goal: Bring all data together for processing.

🧩 Example: Reading customer data from SQL and transaction logs into a single dataset.

2️⃣ Data Validation

What happens:
You check data quality — ensuring it’s complete, consistent, and accurate.
You detect missing values, invalid formats, outliers, or schema mismatches.
Goal: Ensure clean, reliable data before modeling.

🧩 Example: Making sure every row has a customer ID and no negative age values.

3️⃣ Data Transformation

What happens:
You prepare the data for training. This includes:

Handling missing values

Encoding categorical columns

Scaling/normalizing numeric data

Feature engineering

Goal: Convert raw data into a suitable format for the ML algorithm.

🧩 Example: Encoding gender as 0/1, normalizing income, creating new “spend per visit” feature.

4️⃣ Model Training

What happens:
You feed the processed data into a machine learning algorithm to learn patterns.
The model adjusts its internal parameters (weights) to best fit the training data.
Goal: Build a model that can generalize to unseen data.

🧩 Example: Training a Random Forest to predict customer churn.

5️⃣ Model Evaluation

What happens:
You test the model’s performance using a validation or test dataset.
Metrics like accuracy, precision, recall, F1-score, RMSE, or AUC are computed.
Goal: Verify that the model performs well and doesn’t overfit.

🧩 Example: Checking that the churn model gives 85% accuracy on test data.

6️⃣ Model Deployment

What happens:
You move the trained model into production so it can make real-world predictions (via API, web app, or scheduled job).
Goal: Make the model accessible to end users or systems.