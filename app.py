from flask import Flask, request, jsonify, render_template
import time
import os
import requests

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'

def only_tables(data_json):
    tables = []
    for page in data_json['pages']:
        for item in page['items']:
            if item['type'] == 'table':
                tables.append(item)
    return tables
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
    time.sleep(5)
    response_final = requests.get(url, headers=headers)
    if response_final.status_code != 200:
        return jsonify({'error': 'Failed to retrieve parsing result', 'details': response_final.text}), 500

    return only_tables(response_final.json())
    #return jsonify(response_final.json())  # Return the JSON result

    
if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
