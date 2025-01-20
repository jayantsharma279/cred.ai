from flask import Flask, request, jsonify, render_template
import time
import pandas as pd
import json
import os
import requests
from openai import OpenAI

#OpenAI API info
client = OpenAI(api_key='sk-3nqsPXuRAwFc5tFHNlmMhA', base_url="https://cmu.litellm.ai")
USER_STR = "user"
SYSTEM_STR = "system"
MSG_STR = "content"
random_seed = 8942764

SYSTEM_MESSAGE = """
You are a loan evaluation assistant. Your role is to analyze a person's or business's bank statement to determine their loan eligibility. You must evaluate factors like incoming credits, debt-to-income ratio, and loan repayment ability based on the provided transactions, amounts, and descriptions.

Your response must include:
1. A clear decision: `<Accepted/Rejected>` for an amount not exceeding `<Credit Limit>`.
2. A justification based on key financial indicators.
3. Suggested improvements if the loan is rejected.
Output your response in the following structured JSON format:
{
  "decision": "<Accepted/Rejected>",
  "credit_limit": "<Max loan amount>",
  "justification": "<Detailed analysis>",
  "recommendations": "<Steps for improvement if rejected>"
}
"""

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'

def only_tables(data_json):
    tables = []
    for page in data_json.get("pages", []):
        for item in page.get("items", []):
            if item.get("type") == "table" and "rows" in item:
                tables.append(item["rows"])
    #df = pd.DataFrame([row for page in data_json["pages"] for item in page["items"] if item.get("type") == "table" for row in item["rows"]])
    return tables

def format_as_readable(json_data):
    formatted_str = "Bank Statement Transactions: [\n"
    for sublist in json_data:
        formatted_str += "  [\n"
        for item in sublist:
            formatted_str += f"    {json.dumps(item)},\n"
        formatted_str = formatted_str.rstrip(",\n") + "\n  ],\n"
    formatted_str = formatted_str.rstrip(",\n") + "\n]"
    formatted_str += '\nResponse: "" '
    return formatted_str

# Home route to serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file uploads and process them
job_id = None

@app.route('/upload', methods=['POST'])
def upload_pdf():
    global job_id
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    # Send the file to the LlamaParse API
    url = "https://api.cloud.llamaindex.ai/api/v1/parsing/upload"
    headers = {'Authorization': 'Bearer llx-4NtZLmrLPlJX6ZQZBN4T1Y9B8Bu2YlQPy8UjaxEJN7PzXYOo'}
    with open(file_path, 'rb') as f:
        response = requests.post(url, headers=headers, files={'file': f})

    if response.status_code != 200:
        return jsonify({'error': 'LlamaParse API error', 'details': response.text}), 500

    response_data = response.json()
    job_id = response_data["id"]  # Store the job_id

    if not job_id:
        return jsonify({'error': 'No job_id available. Upload a file first.'}), 400

    url = f"https://api.cloud.llamaindex.ai/api/v1/parsing/job/{job_id}/result/json"
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer llx-4NtZLmrLPlJX6ZQZBN4T1Y9B8Bu2YlQPy8UjaxEJN7PzXYOo'
    }
    
    while True:
        response_final = requests.get(url, headers=headers)   
        if response_final.status_code == 200: #Job is done, give the output
            result  = format_as_readable(only_tables(response_final.json()))

            #print(f"Formatted Result: {result}")  # Debugging log
            BANK_STATEMENT_PROMPT = result
            # Send the result to OpenAI API

            try:
                messages = [{"role": "system", "content": SYSTEM_MESSAGE},
                    {"role": "user", "content": BANK_STATEMENT_PROMPT}]
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    temperature=0.0,
                    seed=random_seed,
                    messages=messages)
                               
                return response.choices[0].message.content
            
            except Exception as e:
                return jsonify({"error": "OpenAI API call failed", "details": str(e)}), 500
        elif response_final.status_code == 422:

            return jsonify({'error': 'Failed to retrieve parsing result', 'details': response_final.text}), 500
        else:

            time.sleep(3)
            # return jsonify({'error': 'Failed to retrieve parsing result', 'details': response_final.text}), 500
            continue
    

            
if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
