from flask import Flask, request, jsonify, render_template
import os
import requests

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'

# Home route to serve the HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file uploads and process them
@app.route('/upload', methods=['POST'])
def upload_pdf():
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

    # Return the parsed JSON data
    return jsonify(response.json())

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
