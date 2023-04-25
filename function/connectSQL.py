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
        try:
            # self.connect = db.connect(
            #     "Driver={SQL Server};"
            #     f"Server={server_name};Database={database_name};Trusted_Connection=yes;"
            # )

            self.connect = db.connect(
                'Driver={SQL Server};'
                f'Server={self.serverName};Database={self.databaseName};UID=sqlserver;PWD=~|YQ4p->-vv*dk\P'
            )

            # connect to cuesor
            self.cursor = self.connect.cursor()

            print("Connect Suscess")

        except db.Error as ex:
            print('Error connecting to : ', ex)

    # def select_query(self, table_name):
    #     try:
    #         query = f'SELECT * FROM {table_name}'
    #         self.cursor.execute(query)
    #
    #         list_query = []
    #         # Check result
    #         for row in self.cursor:
    #             # print(f'Result [{row[0]}] {row[1]} {row[2]}')
    #             list_query.append({
    #                 'id': row[0],
    #                 'name': row[1],
    #                 'age': row[2]
    #             })
    #
    #         return list_query
    #
    #     except db.Error as ex:
    #         print('Error Select table : ', ex)

    def chek_login(self, user, password):
        try:
            # connect database
            self.connect_database()
            # convert md5
            MD5Password = self.convertMD5(password)
            query = f"SELECT * FROM host WHERE username = {user} AND password = {MD5Password}"
            self.cursor.execute(query)
            print(self.cursor.fetchval())
            self.connect.close()
            return
        except db.Error as ex:
            print(f'Error => {ex}')

    def insert_data(self, table_name, dataTarget):
        result = {'message': ''}
        try:
            # convert String to Json
            json_datas = json.loads(dataTarget)
            # convert password MD5
            json_datas['password'] = self.convertMD5(json_datas['password'])
            value_list = [json_datas[field] for field in json_datas if field != 'id_admin']
            # value_list = []
            # for field in json_data:
            #     if field != 'id_admin':
            #         value_list.append(json_data[field])
            # print(value_list)

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
            self.connect.close()

            result['message'] = 'Success'
            print(result['message'])
            return result
        except db.Error as ex:
            print('Error => ', ex)
            result['message'] = f'Error => {ex}'
            return result

    def convertMD5(self, password):
        return hashlib.md5(password.encode()).hexdigest()
