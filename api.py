import os
import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'REPORT_DATA1.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return "Welcome to the Flask API"

@app.route('/latest', methods=['GET'])
def get_latest_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM report_table ORDER BY date_temps DESC LIMIT 1")
        latest_data = cursor.fetchone()
        conn.close()
        if latest_data:
            return jsonify(dict(latest_data))
        else:
            return jsonify({"error": "No data found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/historical', methods=['GET'])
def get_historical_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM report_table")
        historical_data = cursor.fetchall()
        conn.close()
        return jsonify([dict(row) for row in historical_data])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/data_by_date', methods=['GET'])
def get_data_by_date():
    date = request.args.get('date')
    if not date:
        return jsonify({"error": "Date parameter is required"}), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM report_table WHERE DATE(date_temps) = ?"
        cursor.execute(query, (date,))
        data_by_date = cursor.fetchall()
        conn.close()
        if data_by_date:
            return jsonify([dict(row) for row in data_by_date])
        else:
            return jsonify({"error": "No data found for the specified date"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
