from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)

def fetch_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.get_text()

def check_compliance_with_gemini(policy_text, company_text):
    try:
        prompt = f"""
        You are a compliance checker. Your task is to analyze the following company's website against a given policy.
        Policy:
        {policy_text}
        Company Website Text:
        {company_text}
        Please provide a detailed analysis of how well the company adheres to the policy. 
        Identify specific areas of compliance and non-compliance. 
        STRICTLY FORMAT YOUR RESPONSE AS A JSON OBJECT WITH THE FOLLOWING STRUCTURE NO MATTER WHAT:
        {{
            "compliant_areas": ["list", "of", "compliant", "areas"],
            "non_compliant_areas": ["list", "of", "non-compliant", "areas"],
            "analysis": {{
                "summary": "Detailed summary of the compliance analysis",
                "recommendations": ["list", "of", "recommendations"]
            }}
        }}
        """

        response = model.generate_content(prompt)
        
        if not response or not response.text:
            raise Exception("Gemini API returned an empty or invalid response.")

        # Use .strip() to remove any leading/trailing whitespace
        llmResponse = response.text.strip().replace('```','').replace('json','')
        print(llmResponse)
        return llmResponse

    except Exception as e:
        raise Exception(f"Gemini API error: {str(e)}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_compliance', methods=['POST'])
def check_policy_compliance():
    try:
        data = request.json
        policy_text = fetch_content(data['policy_url'])
        company_text = fetch_content(data['company_url'])

        # Debug: Print or log the fetched content to check if it's valid
        print("Policy Text:", policy_text)
        print("Company Text:", company_text)

        # If either text is empty, return an error
        if not policy_text or not company_text:
            return jsonify({
                "isSuccess": False,
                "error": "Fetched content is empty or invalid.",
                "data": None
            }), 400
        
        compliance_report = check_compliance_with_gemini(policy_text, company_text)

        # Rest of the code for formatting the response
        compliance_report_json = json.loads(compliance_report)  # Convert Gemini response string to JSON object
        print('compliance_report: ',compliance_report)

        formatted_response = {
            "isSuccess": True,
            "error": None,
            "data": {
                "compliant_areas": compliance_report_json['compliant_areas'],
                "non_compliant_areas": compliance_report_json['non_compliant_areas'],
                "analysis": {
                    "summary": compliance_report_json['analysis']['summary'],
                    "recommendations": compliance_report_json['analysis']['recommendations']
                }
            }
        }
        print('formatted response: ', formatted_response)
        return jsonify(formatted_response), 200
    
    except Exception as e:
        return jsonify({
            "isSuccess": False,
            "error": str(e),
            "data": None
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
