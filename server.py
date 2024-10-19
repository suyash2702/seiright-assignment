from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException
from pydantic import BaseModel, HttpUrl
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__)

class UrlInput(BaseModel):
    policy_url: HttpUrl
    company_url: HttpUrl

def fetch_content(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.get_text()

def check_compliance_with_openai(policy_text, company_text):
    prompt = f"""
    You are a compliance checker. Your task is to analyze the following company's text against a given policy.
    Policy:
    {policy_text}
    Company Text:
    {company_text}
    Please provide a detailed analysis of how well the company text adheres to the policy. 
    Identify specific areas of compliance and non-compliance. 
    Format your response as a JSON object with the following structure:
    {{
        "compliant_areas": ["list", "of", "compliant", "areas"],
        "non_compliant_areas": ["list", "of", "non-compliant", "areas"],
        "analysis": "Detailed explanation of the compliance analysis"
    }}
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that analyzes compliance."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

@app.route('/check_compliance', methods=['POST'])
def check_policy_compliance():
    try:
        data = request.json
        url_input = UrlInput(**data)
        policy_text = fetch_content(url_input.policy_url)
        company_text = fetch_content(url_input.company_url)
        
        compliance_report = check_compliance_with_openai(policy_text, company_text)
        
        return jsonify(compliance_report), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)