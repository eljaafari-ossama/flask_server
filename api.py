from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# Configuration de la base de données MySQL
DB_CONFIG = {
    'host': 'localhost',      # Remplacez par votre hôte MySQL
    'user': 'root',  # Remplacez par votre utilisateur MySQL
    'password': '1234',  # Remplacez par votre mot de passe MySQL
    'database': 'report_database'  # Remplacez par le nom de votre base de données
}

# Connexion à la base de données
def get_db_connection():
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn

@app.route('/', methods=['GET'])
def welcome():
    return 'welcome'
@app.route('/data/latest', methods=['GET'])
def get_latest_data():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM report_table ORDER BY date_temps DESC LIMIT 1")
    data = cursor.fetchone()
    cursor.close()
    conn.close()
    return jsonify(data)

@app.route('/data/historical', methods=['GET'])
def get_historical_data():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM report_table WHERE date_temps BETWEEN %s AND %s"
    cursor.execute(query, (start_date, end_date))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
