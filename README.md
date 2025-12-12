# Attrition Analytics for IBM – End-to-End AI-Enabled Workforce Stability Project

This repository contains an end-to-end **employee attrition analytics** project developed as part of the AI-Integrated Strategy Management Project for the EMBA program at IIM Ranchi.


## 1. Repository Structure (You can ignore this and find the structure in the github repo link provided in the Project Report.)

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

-------------------------------------------------------------------------

2. How to setup the Application in 5 steps:

Prerequisites

Please ensure the following software is installed:
-Python 3.9+
-Git
-Power BI Desktop (for opening the .pbix dashboard)
-Visual Studio Code (recommended editor)
-------------------------------------------
Step -1  Clone the repository

1- Open Powershell as Administrator:
 - Navigate to your desktop path 
 (comand : cd C:\your_desktop_path_here)

 - make a new folder here called attrition_app_test 
 (command: mkdir attrition_app_test)
 or you can do this manually on the desktop-> right click -> create folder -> name it attrition_app_test

 - navigate inside this folder from powershell: 
 (command: cd .\attririon_app_test\)
----------------------------------------------

Step 2 - Create a new virtual environment:

 - inside the attrition_app_test use 
 (command: python -m venv app_test) for windows users and mac both
    This will create a virtual test environment

 - Activate the environment using 
 (command: app_test/Scripts/activate) for windows users
 (command: source venv/bin/activate) for mac users.

 You should now see (app_test) at the beginning of your terminal prompt, something like this: 
 (app_test) PS C:\Users\Sarva\Desktop\attrition_app_test>
-----------------------------------------------------

Step 3 - Clone the GitHub repository:
3.1- inside this path '\Desktop\attrition_app_test' (Yours would be different before 'Desktop') Run the command:
 (- Command : git clone https://github.com/sarvagyamehrotra/Attrition-Analytics-IBM.git)
------------------------------------------------------

3.2 Install Python Dependencies: execute the following commands in the vscode terminal:

1- Navigate to the newly created Attrition-Analytics-IBM folder after git clone inside the attrition_app_test folder.
(command: cd .\Attrition-Analytics-IBM\)
------------------------------------------------------

Step 4- Install requirements from requirements.txt using
 (commmand: pip install -r requirements.txt)
wait for the installation to complete. The cursor will keep blinking while installing. Once installed you will this on the terminal:
(app_test) PS C:\Users\Sarva\Desktop\attrition_app_test\Attrition-Analytics-IBM> 
---------------------------------------------------------------------------------------------------
Step 5- Run the app: (Note: If you want LLM integration then execute step 6 before step 5)
-  When inside this path .\Desktop\attrition_app_test\Attrition-Analytics-IBM execute the command:
(command: python app.py)

this will launch the server and display the server link where the app is hosted.
Simply copy and paste the URL in any browser and hit enter.

--------------------------------------------------------------------------------
Step 6- LLM integration with the OpenAI API:

Configure the OpenAI API Key (for LLM suggestions)

The app uses OpenAI’s API to generate HR Strategy actions based on the model’s predictions and SHAP explanations.
To enable this feature:
- Obtain an OpenAI API key from your OpenAI account. Log in to the API key platform from OpenAI page and go to your profile. Navigate to API key section and generate a new secret key. Copy this key
- Set an environment variable named OPENAI_API_KEY.
Command (Windows PowerShell): $env:OPENAI_API_KEY = "your_api_key_here" (your key should be insde the inverted commas)
Command (macOS / Linux): export OPENAI_API_KEY="your_api_key_here"

If OPENAI_API_KEY is not set, the web app will still run, but the LLM-based suggestion box will show a message indicating that suggestions are disabled.

---------------------------------------------------------------------------------

7 - Using the Power BI Dashboard:
The Power BI dashboard is located at:
dashboards/Attrition_Dashboard.pbix

Steps to open and explore:
Open Power BI Desktop.
Go to File → Open and select Attrition_Dashboard.pbix.
If prompted for file locations, point Power BI to the data/attrition_scores.csv file inside this project folder.
Click Refresh on the Home ribbon to make sure the latest data is loaded.
Explore the dashboard pages:
Overall attrition overview
Department-wise and job-role-wise risk
Distribution of probability scores
Drill-down views for specific segments or employees
The dashboard is designed to give a high-level view of workforce stability and highlight high-risk groups.
-----------------------------------------------------------------------------------

8 - Using the Web UI

Open a browser and go to the URL displayed after executing python app.py
Fill in the employee details on the form (distance from home, years at company, job role, department, etc.).
Click the Predict button.
The app will:
Load the trained XGBoost model from models/attrition_xgb_model.pkl.
Predict the attrition probability for the entered employee.
Display the probability and key SHAP drivers in a human-readable format.
If an OpenAI key is configured:
Generate suggested next steps for HR to retain the employee or manage the risk.
The UI is designed so that a non-technical HR user can easily interpret the results.

------------------------------------------------------------------------------------

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