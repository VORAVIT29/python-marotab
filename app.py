import json

from flask import Flask, request, jsonify
from flask_cors import CORS
from function import func, connectSQL

app = Flask(__name__)
CORS(app)

# Connect Sql
# Local Server
# sql = connectSQL.SQL('DESKTOP-R4AEEG6\SQLEXPRESS', 'testDatabase')
# Server Cloud
sql = connectSQL.SQL('35.240.177.233', 'marotabBeta')


@app.route('/api/get-data', methods=['POST'])
def select_data():
    data_id = request.json
    # print('Id =>', data_id['idHost'])

    # data = request.get_json()
    # print(data['message'])

    # Query Table
    dataQuery = sql.select_query('host')
    # print(dataQuery)

    return jsonify(dataQuery)


@app.route('/api/insert-login', methods=['POST'])
def insert_login():
    data = request.json
    dataTarget = data['target']
    tableName = data['table']

    # print(dataTarget)
    result = sql.insert_data(tableName, dataTarget)
    return jsonify(result)


@app.route('/api/check-login', methods=['POST'])
def check_login():
    data = request.json
    user = data['username']
    password = data['password']
    print(user, password)
    
    return ''


if __name__ == '__main__':
    # app.run(debug=True, host='localhost', port=3000)
    app.run(debug=True)
