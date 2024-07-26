from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# Configuration de la base de données MySQL
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'report_database'
}

# Fonction pour se connecter à la base de données MySQL
def get_db_connection():
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn

# Route pour récupérer les données les plus récentes
@app.route('/latest', methods=['GET'])
def get_latest_data():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM report_table ORDER BY date_temps DESC LIMIT 1")
    latest_data = cursor.fetchone()
    conn.close()
    
    if latest_data:
        return jsonify(latest_data)
    else:
        return jsonify({"error": "No data found"}), 404

# Route pour récupérer les données historiques
@app.route('/historical', methods=['GET'])
def get_historical_data():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM report_table ORDER BY date_temps DESC")
    historical_data = cursor.fetchall()
    conn.close()
    
    if historical_data:
        return jsonify(historical_data)
    else:
        return jsonify([]), 404

if __name__ == '__main__':
    app.run(debug=True)
