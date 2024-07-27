from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# Configuration de la base de données MySQL
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'report_database'
}

# Connexion à la base de données
def get_db_connection():
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn

# Fonction pour convertir une ligne de données en dictionnaire
def row_to_dict(cursor, row):
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))

@app.route('/', methods=['GET'])
def welcome():
    return 'Welcome to the API!'

# Route pour récupérer les données les plus récentes
@app.route('/latest', methods=['GET'])
def get_latest_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM report_table ORDER BY date_temps DESC LIMIT 1")
        latest_data = cursor.fetchone()
        conn.close()
        if latest_data:
            return jsonify(row_to_dict(cursor, latest_data))
        else:
            return jsonify({"error": "No data found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route pour récupérer les données historiques
@app.route('/historical', methods=['GET'])
def get_historical_data():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM report_table")
        historical_data = cursor.fetchall()
        conn.close()
        return jsonify([row_to_dict(cursor, row) for row in historical_data])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route pour récupérer les données pour une date spécifique
@app.route('/data_by_date', methods=['GET'])
def get_data_by_date():
    date = request.args.get('date')
    if not date:
        return jsonify({"error": "Date parameter is required"}), 400
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM report_table WHERE DATE(date_temps) = %s"
        cursor.execute(query, (date,))
        data_by_date = cursor.fetchall()
        conn.close()
        if data_by_date:
            return jsonify([row_to_dict(cursor, row) for row in data_by_date])
        else:
            return jsonify({"error": "No data found for the specified date"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
