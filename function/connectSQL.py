import json
import hashlib
import pyodbc as db


class SQL:
    connect = None
    cursor = None
    serverName = ''
    databaseName = ''

    def __init__(self, server_name, database_name):
        self.serverName = server_name
        self.databaseName = database_name

        # connect to database
        self.connect_database()

    def connect_database(self):
        result = {'status': '', 'result': None}
        try:
            # ODBC Driver 17 for SQL Server
            # self.connect = db.connect(
            #     "Driver={ODBC Driver 17 for SQL Server};"
            #     f"Server={self.serverName};Database={self.databaseName};Trusted_Connection=yes;"
            # )

            self.connect = db.connect(
                'Driver={SQL Server};'
                f'Server={self.serverName};Database={self.databaseName};UID=sqlserver;PWD=~|YQ4p->-vv*dk\P'
            )

            # connect to cuesor
            self.cursor = self.connect.cursor()

            print("Connect Suscess")
            result['result'] = "Connect Suscess"
            return result

        except db.Error as ex:
            print('Error connecting to : ', ex)
            result['result'] = 'Error connecting to : ', ex
            return result

    def findUserPassByAdminPass(self, admin_pass):
        result = {'status': '', 'result': None}
        try:
            query = f"SELECT id_admin,username FROM host WHERE admin_password = '{admin_pass}' "
            self.cursor.execute(query)
            data_list = self.cursor.fetchall()

            if len(data_list) > 0:
                dict_ = {
                    'id_admin': data_list[0][0],
                    'username': data_list[0][1]
                }
                # return list_query
                result['status'] = 'Success'
                result['result'] = dict(dict_)
            else:
                # return list_query
                result['status'] = 'Error'
                result['result'] = 'ไม่พบข้อมูล'
            return result

        except db.Error as ex:
            print('Error Select table : ', ex)
            result['status'] = 'Error'
            result['result'] = f'Error Select table : {ex}'
            return result

    def chek_login(self, user, password):
        result = {'message': ''}
        try:
            # connect database
            # self.connect_database()

            # convert md5
            MD5Password = self.convertMD5(password)
            query = f"SELECT * FROM host WHERE username = '{user}' AND password = '{MD5Password}' "
            self.cursor.execute(query)
            # self.connect.close()

            result['message'] = str(self.cursor.fetchval())
            return result
        except db.Error as ex:
            print(f'Error => {ex}')
            result['message'] = f'Error => {ex}'
            return result

    def chenge_password(self, new_password, id_admin):
        result = {'message': ''}
        try:
            pass_md5 = self.convertMD5(new_password)
            query_change = f"UPDATE host SET password = '{pass_md5}' WHERE id_admin = {id_admin} "
            self.cursor.execute(query_change)
            self.connect.commit()
            result['message'] = 'Success'
            return result
        except db.Error as ex:
            result['message'] = f'Error => {ex}'
            return result

    def insert_data(self, table_name, dataTarget):
        result = {'message': ''}
        try:
            # connect database
            # self.connect_database()
            # convert String to Json
            json_datas = json.loads(dataTarget)
            # convert password MD5
            json_datas['password'] = self.convertMD5(json_datas['password'])
            value_list = [json_datas[field] for field in json_datas if field != 'id_admin']
            # convert List to String
            value_list_toStr = ','.join([f'\'{elem}\'' for elem in value_list])
            # Query insert
            insert_data = f"INSERT INTO {table_name} VALUES ({value_list_toStr})"
            # print(insert_data)
            # excute query
            self.cursor.execute(insert_data)
            # เปลี่ยนแปลงข้อมูล
            self.connect.commit()
            # ปิดการเชิ่มต่อ
            # self.connect.close()

            result['message'] = 'Success'
            print(result['message'])
            return result
        except db.Error as ex:
            print('Error => ', ex)
            result['message'] = f'Error => {ex}'
            return result

    def find_all(self, table_name):
        query_all = f"SELECT * FROM {table_name}"
        self.cursor.execute(query_all)
        return self.cursor.fetchall()

    def convertMD5(self, password):
        return hashlib.md5(password.encode()).hexdigest()
