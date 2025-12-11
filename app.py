
import os

from flask import Flask, render_template, request
import pandas as pd
import joblib
import shap
import numpy as np
from openai import OpenAI

client = OpenAI()
app = Flask(__name__)

# ---------- 1. Load your saved pipeline ----------
MODEL_PATH = os.path.join("models", "attrition_xgb_model.pkl")
final_pipeline = joblib.load(MODEL_PATH)

FEATURE_ORDER = [
    'Age',
    'DistanceFromHome',
    'EnvironmentSatisfaction',
    'JobLevel',
    'JobSatisfaction',
    'MonthlyIncome',
    'NumCompaniesWorked',
    'TotalWorkingYears',
    'YearsAtCompany',
    'YearsInCurrentRole',
    'YearsWithCurrManager',
    'JobRole',
    'MaritalStatus',
    'OverTime'
]

def generate_llm_suggestions(probability, shap_top, employee_inputs):
    """
    Call the LLM to generate retention suggestions for HR.
    probability: float (0–100, %)
    shap_top: list of dicts with keys: name, direction, value
    employee_inputs: original input_dict (Age, JobRole, OverTime, etc.)
    """
    try:
        # Summarise key drivers in text
        driver_lines = []
        for item in shap_top:
            driver_lines.append(
                f"- {item['name']} ({item['direction']} attrition risk, SHAP = {item['value']:.3f})"
            )
        drivers_text = "\n".join(driver_lines)

        # Some core fields for context
        core_ctx = f"""
Age: {employee_inputs.get('Age')}
Job Role: {employee_inputs.get('JobRole')}
Marital Status: {employee_inputs.get('MaritalStatus')}
OverTime: {employee_inputs.get('OverTime')}
Years at Company: {employee_inputs.get('YearsAtCompany')}
Job Satisfaction (1–4): {employee_inputs.get('JobSatisfaction')}
Environment Satisfaction (1–4): {employee_inputs.get('EnvironmentSatisfaction')}
        """.strip()

        prompt = f"""
You are an HR analytics assistant. You help HR managers interpret an attrition prediction model and decide practical next steps.

Model output:
- Predicted probability that the employee will leave: {probability:.2f}%

Employee context:
{core_ctx}

Top factors driving the prediction (from SHAP values):
{drivers_text}

Task:
Write 4–6 concrete and ethical recommendations for HR on how to reduce attrition risk for THIS employee.

Guidelines:
- Be specific and practical (e.g., "schedule a 1:1 conversation to discuss workload within 2 weeks").
- Tie recommendations back to the factors when relevant (e.g., high overtime → adjust workload).
- Keep it HR-friendly, no technical jargon, no mention of SHAP or machine learning.
- Use short bullet points.
"""
        response = client.responses.create(
            model="gpt-4.1-mini",   # or "gpt-5.1-mini" if available in your account
            input=prompt,
            max_output_tokens=350,
        )

        # SDK convenience: aggregated text
        suggestions_text = response.output_text
        return suggestions_text

    except Exception as e:
        # Don't crash the app if API fails
        return f"(Could not generate AI suggestions: {e})"


@app.route("/", methods=["GET", "POST"])
def home():
    probability = None
    form_data = {}
    shap_top = []      # list of top SHAP factors
    suggestions = None # placeholder for LLM output later



    if request.method == "POST":
        try:
            job_role = request.form['JobRole']

            # Map new roles to existing categories the encoder knows
            if job_role == "Developer":
            # treat Developer as an R&D role – choose what makes sense to you
                job_role = "Research Scientist"   # or "Laboratory Technician" / "Research Director"

            input_dict = {
                'Age': float(request.form['Age']),
                'DistanceFromHome': float(request.form['DistanceFromHome']),
                'EnvironmentSatisfaction': float(request.form['EnvironmentSatisfaction']),
                'JobLevel': float(request.form['JobLevel']),
                'JobSatisfaction': float(request.form['JobSatisfaction']),
                'MonthlyIncome': float(request.form['MonthlyIncome']),
                'NumCompaniesWorked': float(request.form['NumCompaniesWorked']),
                'TotalWorkingYears': float(request.form['TotalWorkingYears']),
                'YearsAtCompany': float(request.form['YearsAtCompany']),
                'YearsInCurrentRole': float(request.form['YearsInCurrentRole']),
                'YearsWithCurrManager': float(request.form['YearsWithCurrManager']),
                'JobRole': job_role,
                'MaritalStatus': request.form['MaritalStatus'],
                'OverTime': request.form['OverTime'],
            }

            PRETTY_LABELS = {
                'Age': 'Age',
                'DistanceFromHome': 'Distance From Home',
                'EnvironmentSatisfaction': 'Environment Satisfaction',
                'JobLevel': 'Job Level',
                'JobSatisfaction': 'Job Satisfaction',
                'MonthlyIncome': 'Monthly Income',
                'NumCompaniesWorked': 'Number of Companies Worked',
                'TotalWorkingYears': 'Total Working Years',
                'YearsAtCompany': 'Years at Company',
                'YearsInCurrentRole': 'Years in Current Role',
                'YearsWithCurrManager': 'Years with Current Manager',
                'JobRole': 'Job Role',
                'MaritalStatus': 'Marital Status',
                'OverTime': 'OverTime'
            }


            form_data = {k: str(v) for k, v in input_dict.items()}

            # DataFrame in correct column order
            X = pd.DataFrame([input_dict], columns=FEATURE_ORDER)

            # ----- 1. Prediction -----
            proba = final_pipeline.predict_proba(X)[0, 1]
            probability = round(proba * 100, 2)

            # ----- 2. SHAP for this single employee -----
            model = final_pipeline.named_steps['model']
            preproc = final_pipeline.named_steps['preprocessing']

            X_transformed = preproc.transform(X)

            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(X_transformed)

            # If we get a list [class0, class1], take class1
            if isinstance(shap_values, list):
                shap_values = shap_values[1]

            shap_for_instance = shap_values[0]  # 1st (and only) row

            feature_names = preproc.get_feature_names_out()

            shap_items = []

            for raw_name, value in zip(feature_names, shap_for_instance):
                val = float(value)

                # raw_name looks like "num__Age" or "cat__OverTime_Yes"
                if "__" in raw_name:
                    prefix, rest = raw_name.split("__", 1)
                else:
                    prefix, rest = "", raw_name

                pretty_name = rest  # fallback

                if prefix == "num":
                    # numeric feature, e.g. "Age"
                    base_feat = rest
                    pretty_name = PRETTY_LABELS.get(base_feat, base_feat)

                elif prefix == "cat":
                    # categorical one-hot, e.g. "OverTime_Yes" or "MaritalStatus_Single"
                    if "_" in rest:
                        base_feat, category = rest.split("_", 1)
                    else:
                        base_feat, category = rest, ""

                    base_label = PRETTY_LABELS.get(base_feat, base_feat)
                    category = category.replace("_", " ")
                    if category:
                        pretty_name = f"{base_label} = {category}"
                    else:
                        pretty_name = base_label
                else:
                # just in case some name doesn't follow the pattern
                    pretty_name = PRETTY_LABELS.get(rest, rest)

                shap_items.append({
                    "raw_name": raw_name,
                    "name": pretty_name,           
                    "value": val,
                    "abs_value": abs(val),
                    "direction": "increases" if val > 0 else "decreases"
                })

            shap_top = sorted(shap_items, key=lambda x: x["abs_value"], reverse=True)[:5]
            # ----- 3. LLM suggestions based on risk + drivers -----
            suggestions = generate_llm_suggestions(probability, shap_top, input_dict)

            print("SHAP TOP:", shap_top)  # debug in terminal



        except Exception as e:
            probability = f"Error while predicting: {e}"
            shap_top = []
            print("Error in prediction/SHAP:", e)

    return render_template(
        "index.html",
        probability=probability,
        shap_top=shap_top,
        suggestions=suggestions,
        form_data=form_data
    )


if __name__ == "__main__":
    app.run(debug=True)
