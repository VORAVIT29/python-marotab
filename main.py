from flask import Flask, request, jsonify
from flask_cors import CORS
from function import connectSQL

app = Flask(__name__)
CORS(app)

# Connect Sql
# Local Server
# sql = connectSQL.SQL('DESKTOP-R4AEEG6\SQLEXPRESS', 'marotab')
# Server Cloud
sql = connectSQL.SQL('35.240.177.233', 'marotabBeta')


# data = request.get_json()
# print(data['message'])

@app.route('/')
def main():
    return '<body style="background:black;color:white">' \
           '<center>' \
           '<br/>' \
           '<h1>Welcome To Python Server <small>UPDATE 5/6/2023</small></h1>' \
           '<h2>Python Version (3.9)</h2>' \
           '<h3>Flask Version (2.2.2)</h3>' \
           f'<p>Status Database: {sql.connect_database()}</p>' \
           '<img src="/static/python.png" width="300" style="padding:5rem;"/>' \
           '</center>' \
           '</body>'


@app.route('/insert-data', methods=['POST'])
def insert_data():
    data = request.json
    dataTarget = data['target']
    tableName = data['table']
    result = sql.insert_data(tableName, dataTarget)
    return jsonify(result)


@app.route('/update-data-call', methods=['POST'])
def update_data_call():
    data = request.json
    dataTarget = data['target']
    tableName = data['table']
    result = sql.update_call(tableName, dataTarget)
    return jsonify(result)


@app.route('/save-img', methods=['POST'])
def save_img():
    data = request.json
    dataTarget = data['target']
    tableName = data['table']
    result = sql.save_img(tableName, dataTarget)
    return jsonify(result)


@app.route('/edit-data-tenantRoom', methods=['POST'])
def edit_data_tenantRoom():
    data = request.json
    dataTarget = data['target']
    result = sql.edit_tenantRoom(dataTarget)
    return jsonify(result)


@app.route('/delete-tenantRoom', methods=['POST'])
def delete_tenant_room_byid():
    data = request.json
    data_target = data['target']
    result = sql.delete_tenantRoom(data_target)
    return jsonify(result)


@app.route('/all-data/<table>')
def find_all(table):
    data_all = sql.find_all(table)
    return jsonify(data_all)


@app.route('/find-data-tenant-byIdNumber/<table_name>/<id>')
def find_data_byIdNumber(id, table_name):
    result = sql.find_data_byId(id, table_name)
    # print('find_data_byIdNumber =>', result)
    return jsonify(result)


@app.route('/find-dataImg-byRoomnumber/<roomNumber>')
def find_dataImg_by_room_number(roomNumber):
    result = sql.find_dataImg_byRoomnumber(roomNumber)
    return jsonify(result)


@app.route('/check-login', methods=['POST'])
def check_login():
    data = request.json
    user = data['username']
    password = data['password']
    result = sql.check_login(user, password)
    # print(f'Check Login => {result}')
    return jsonify(result)


@app.route('/change-forget-password', methods=['POST'])
def change_forget_pass():
    data = request.json
    id_admin = data['id_admin']
    new_password = data['password']
    result = sql.change_password(new_password, id_admin)
    # print(f'Change Password => {result}')
    return jsonify(result)


@app.route('/findUserPass-byAdminPass', methods=['POST'])
def find_by_adminPass():
    data = request.json
    admin_pass = data['admin_password']
    dataQuery = sql.findUserPassByAdminPass(admin_pass)
    # print(f'findUser byadminpass => {dataQuery}')
    return jsonify(dataQuery)


@app.route('/find-data-call-miter/<room_number>')
def find_data_call_miter(room_number):
    result = sql.find_data_call_miter_byId(room_number)
    # print('find_data_call_miter =>', result)
    return jsonify(result)


@app.route('/find-callmiter-list/<room_number>')
def find_callmiter_lists(room_number):
    result = sql.find_callmiter_lists_by_roomnumber(room_number)
    return jsonify(result)


if __name__ == '__main__':
    # app.run(debug=True, host='localhost', port=3000)
    app.run(debug=True)
