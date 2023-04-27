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


# data = request.get_json()
# print(data['message'])

@app.route('/insert-login', methods=['POST'])
def insert_login():
    data = request.json
    dataTarget = data['target']
    tableName = data['table']
    # print(dataTarget)
    result = sql.insert_data(tableName, dataTarget)
    print(f'Insert Login => {result}')
    return jsonify(result)


@app.route('/check-login', methods=['POST'])
def check_login():
    data = request.json
    user = data['username']
    password = data['password']
    result = sql.chek_login(user, password)
    print(f'Check Login => {result}')
    return jsonify(result)


@app.route('/change-forget-password', methods=['POST'])
def change_forget_pass():
    data = request.json
    id_admin = data['id_admin']
    new_password = data['password']
    result = sql.chenge_password(new_password, id_admin)
    print(f'Change Password => {result}')
    return jsonify(result)


@app.route('/findUserPass-byAdminPass', methods=['POST'])
def find_by_adminPass():
    data = request.json
    admin_pass = data['admin_password']
    dataQuery = sql.findUserPassByAdminPass(admin_pass)
    print(f'findUser byadminpass => {dataQuery}')
    return jsonify(dataQuery)


@app.route('/select-unit-byId', methods=['POST'])
def select_unit_byId():
    data = request.json
    id = data['id']
    return ''


if __name__ == '__main__':
    # app.run(debug=True, host='localhost', port=3000)
    app.run(debug=True)
