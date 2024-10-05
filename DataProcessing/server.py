from flask import Flask, jsonify, request
from flask_cors import CORS

from summarization import summarize_topic_by_index
from summarization import getPdfName
from app import api_run_query
#app instance
app = Flask(__name__)
CORS(app)
# Example data - you can replace this with database calls
reports = [
    {"id": 1, "title": "Annual Report 2023", "content": "Details of the 2023 annual report..."},
    {"id": 2, "title": "Quarterly Report Q1 2023", "content": "Details of the first quarter..."},
]

@app.route("/api/home", methods=['GET'])
def return_home():
    return jsonify({
        'message':'HELLO WORLD'
    })
# This is for posting data to the API
@app.route('/api/reports', methods=['POST'])
def add_report():
    new_report = request.json
    new_report["id"] = len(reports) + 1  # Auto-increment ID for simplicity
    reports.append(new_report)
    return jsonify(new_report), 201

# Route to summarize a report section based on topic_index passed as a URL parameter
@app.route('/api/summarize/<int:topic_index>/<int:topic_part>', methods=['GET'])
def summarize_report(topic_index, topic_part):

    topic_part = topic_part + 1
    pdf_path = getPdfName(topic_part)
    summary = summarize_topic_by_index(pdf_path, topic_index, topic_part)

    return jsonify({
        'message': summary
    })

@app.route('/api/bot/<string:prompt>', methods=['GET'])
def get_message(prompt):
    response = api_run_query(prompt)

    return jsonify({
        'prompt' : response
    })


if __name__ == '__main__':
    app.run(debug=True, port=8080)