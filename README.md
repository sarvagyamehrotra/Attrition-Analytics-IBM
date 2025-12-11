# Attrition Analytics for IBM – End-to-End AI-Enabled Workforce Stability Project

This repository contains an end-to-end **employee attrition analytics** project developed as part of the AI-Integrated Strategy Management Project for the EMBA program at IIM Ranchi.


## 1. Repository Structure

```text
.
├─ app.py                          # Flask application entry point
├─ requirements.txt                # Python dependencies
├─ README.md                       # Project documentation (this file)
├─ data/
│   Attrition_Data.csv             # Original IBM HR attrition dataset
│   attrition_scores.csv           # Dataset with model-predicted probability scores
├─ models/
│   attrition_xgb_model.pkl        # Final trained XGBoost model used by the app
│   old_attrition_xgb_model.pkl    # (Optional) older/experimental model
├─ notebooks/
│   Employee Attrition Analytics.ipynb        # EDA + feature engineering + model building
│   probability_scores_dashboard_data.ipynb   # Generates probability scores for each employee
├─ dashboards/
│   Attrition_Dashboard.pbix       # Power BI dashboard built on attrition_scores.csv
├─ templates/
│   index.html                     # Main HTML template for the web form + results
│   (other HTML templates, if any)
├─ static/
│   css/, js/, images/             # Static assets for the web UI (if used)
└─ .gitignore                      # Files and folders excluded from Git

---

## 2. How to setup the project

2.1. Prerequisites

Please ensure the following software is installed:
-Python 3.9+
-Git
-Power BI Desktop (for opening the .pbix dashboard)
-Visual Studio Code (recommended editor)

2.2. Clone the Repository

Open a terminal (or PowerShell) and run:

git clone https://github.com/sarvagyamehrotra/Attrition-Analytics-IBM.git
cd Attrition-Analytics-IBM

All subsequent commands assume you are inside this project folder.

2.3. Create and Activate a Virtual Environment (recommended)

On Windows (PowerShell): execute the following commands

python -m venv venv
venv\Scripts\activate

On macOS / Linux:
python -m venv venv
source venv/bin/activate

You should now see (venv) at the beginning of your terminal prompt.

2.4. Install Python Dependencies: execute the following command in the vscode terminal
pip install -r requirements.txt

This will install all required libraries for:
Data loading and EDA
Model training and prediction (XGBoost, scikit-learn, SHAP)
The Flask web application
Jupyter notebooks
LLM integration with the OpenAI API

---
3. Working with the Jupyter Notebooks

The notebooks are in the notebooks/ folder.
3.1. Starting Jupyter
From the project root (with the virtual environment activated):
jupyter notebook
A browser window will open. Navigate to the notebooks folder and open:
Employee Attrition Analytics.ipynb
probability_scores_dashboard_data.ipynb
You can also open these notebooks directly inside VS Code if the Python and Jupyter extensions are installed.

3.2. Notebook 1: Employee Attrition Analytics

This notebook performs the following:
Loads data/Attrition_Data.csv
Conducts exploratory data analysis (EDA):
Summary statistics
Distributions of key variables
Correlations between features and attrition
Visualizations for important patterns
Performs data preprocessing and feature engineering
Trains an XGBoost classifier to predict attrition (Yes/No)
Evaluates the model using appropriate classification metrics
Uses SHAP to:
Identify global feature importance
Interpret individual predictions
Running this notebook from top to bottom will reproduce the model-building pipeline and the reasoning behind the selected model.

3.3. Notebook 2: Probability Scores for Dashboard

probability_scores_dashboard_data.ipynb:
Loads the final trained model from models/attrition_xgb_model.pkl
Applies the model to each employee in the dataset
Computes predicted probability of attrition for each employee
Saves the results into data/attrition_scores.csv
The Power BI dashboard uses attrition_scores.csv as its main data source.

4. Using the Power BI Dashboard
The Power BI dashboard is located at:
dashboards/Attrition_Dashboard.pbix

Steps to open and explore:
Open Power BI Desktop.
Go to File → Open and select Attrition_Dashboard.pbix.
If prompted for file locations, point Power BI to the data/Attrition_Data.csv and data/attrition_scores.csv files inside this project folder.
Click Refresh on the Home ribbon to make sure the latest data is loaded.
Explore the dashboard pages:
Overall attrition overview
Department-wise and job-role-wise risk
Distribution of probability scores
Drill-down views for specific segments or employees
The dashboard is designed to give a high-level view of workforce stability and highlight high-risk groups.

5. Running the Flask Web Application (Localhost)

The Flask app provides an HR-friendly interface to check attrition risk for a single employee.

5.1. Open the Project in VS Code:
Start Visual Studio Code.
Choose File → Open Folder… and select the cloned repository folder (Attrition-Analytics-IBM).
Open the integrated terminal (View → Terminal).
Activate the virtual environment if it is not already active.

5.2. Configure the OpenAI API Key (for LLM suggestions)

The app uses OpenAI’s API to generate suggested HR actions based on the model’s predictions and SHAP explanations.
To enable this feature:
Obtain an OpenAI API key from your OpenAI account.
Set an environment variable named OPENAI_API_KEY.
Example (Windows PowerShell): $env:OPENAI_API_KEY = "your_api_key_here"
Example (macOS / Linux): export OPENAI_API_KEY="your_api_key_here"

If OPENAI_API_KEY is not set, the web app will still run, but the LLM-based suggestion box will show a message indicating that suggestions are disabled.

5.3. Start the Flask App: execute the following command in app.py terminal view
python app.py

5.4. Using the Web UI

Open a browser and go to http://127.0.0.1:5000/.
Fill in the employee details on the form (distance from home, years at company, job role, department, etc.).
Click the Predict button.
The app will:
Load the trained XGBoost model from models/attrition_xgb_model.pkl.
Predict the attrition probability for the entered employee.
Display the probability and key SHAP drivers in a human-readable format.
If an OpenAI key is configured:
Generate suggested next steps for HR to retain the employee or manage the risk.
The UI is designed so that a non-technical HR user can easily interpret the results.

6. Reproducing the Probability Scores Pipeline

If you wish to regenerate the probability scores from scratch:
Run Employee Attrition Analytics.ipynb to (re)train the model and save attrition_xgb_model.pkl into models/.
Run probability_scores_dashboard_data.ipynb to:
Load the latest model
Compute updated probability scores
Write a new data/attrition_scores.csv
Open the Power BI file and click Refresh to update the dashboard.

7. Notes for Reviewers / Professors

All core steps (EDA, feature engineering, model training, probability scoring, dashboard design, and app integration) are visible and reproducible from this repository.
The only external secret required is the OpenAI API key for enabling the LLM-based suggestion feature; this is configured locally via the OPENAI_API_KEY environment variable and is not included in this repository for security reasons.
The project demonstrates:
Data understanding and preprocessing
Supervised machine learning (XGBoost)
Model explainability (SHAP)
Visualization and dashboarding (Power BI)
Web application development (Flask)
Integration of predictive models with LLMs for decision support
Please feel free to explore the notebooks, dashboard, and web app in any order; each component is documented and intended to be self-explanatory.