from function.dataStatic import *
import pyodbc as db
import hashlib
import json


class SQL:
    result = {'status': '', 'result': None}
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
            #     "Driver={ODBC Driver 17 for SQL Server};"
            #     f"Server={self.serverName};Database={self.databaseName};Trusted_Connection=yes;"
            # )

            self.connect = db.connect(
                'Driver={ODBC Driver 17 for SQL Server};'
                f'Server={self.serverName};Database={self.databaseName};UID=sqlserver;PWD=~|YQ4p->-vv*dk\P'
            )

            # connect to cuesor
            self.cursor = self.connect.cursor()

            self.set_result('Suscess', 'Connect Suscess')
            return self.result

        except db.Error as ex:
            print('Error connecting to : ', ex)
            self.set_result('Error', f'Error connecting to : {ex}')
            return self.result

    def findUserPassByAdminPass(self, admin_pass):
        # result = {'status': '', 'result': None}
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
                self.set_result(STATUS_SUCCESS, dict(dict_))
            else:
                # return list_query
                self.set_result(STATUS_ERROR, 'ไม่พบข้อมูล')
            return self.result

        except db.Error as ex:
            print('Error Select table : ', ex)
            self.set_result(STATUS_ERROR, f'Error Select table : {ex}')
            return self.result

    def check_login(self, user, password):
        try:
            # convert md5
            MD5Password = self.convertMD5(password)
            query = f"SELECT * FROM host WHERE username = '{user}' AND password = '{MD5Password}' "
            self.cursor.execute(query)

            self.set_result(STATUS_SUCCESS, str(self.cursor.fetchval()))
            return self.result
        except db.Error as ex:
            print(f'Error => {ex}')
            self.set_result(STATUS_ERROR, f'Error => {ex}')
            return self.result

    def change_password(self, new_password, id_admin):
        try:
            pass_md5 = self.convertMD5(new_password)
            query_change = f"UPDATE host SET password = '{pass_md5}' WHERE id_admin = {id_admin} "
            self.cursor.execute(query_change)
            self.connect.commit()
            # set status
            self.set_result(STATUS_SUCCESS)
            return self.result
        except db.Error as ex:
            self.set_result(STATUS_ERROR, f'Error => {ex}')
            return self.result

    def insert_data(self, table_name, dataTarget):
        try:
            # convert String to Json
            json_datas = json.loads(dataTarget)

            if table_name == "host":
                # convert password MD5
                json_datas['password'] = self.convertMD5(
                    json_datas['password'])
            elif table_name == 'Tenant_registration':
                # update status room tenant
                self.update_status_room(json_datas['room_number'], True)

            # [json_datas[field] for field in json_datas if field != 'id_admin']
            value_list = [json_datas[field] for field in json_datas]

            print(value_list)
            # convert List to String
            value_list_toStr = ','.join(
                [elem if type(elem) == int else f'\'{elem}\'' for elem in value_list])

            # Query insert
            insert_data = f"INSERT INTO {table_name} VALUES ({value_list_toStr}) "

            # excute query
            self.cursor.execute(insert_data)

            # เปลี่ยนแปลงข้อมูล
            self.connect.commit()

            # ปิดการเชิ่มต่อ
            # self.cursor.close()
            # self.connect.close()

            self.set_result(STATUS_SUCCESS)
            # print(self.result['status'])
            return self.result
        except db.Error as ex:
            print('Error => ', ex)
            self.set_result(STATUS_ERROR, f'Error => {ex}')
            return self.result

    def edit_tenantRoom(self, data_edit):
        try:
            data_json = json.loads(data_edit)
            # print(data_json)
            sql = "UPDATE Tenant_registration " \
                  f"SET room_number='{data_json['room_number']}',chek_in='{data_json['chek_in']}',chek_out='{data_json['chek_out']}'," \
                  f"status_date='{data_json['status_date']}',id_card_number='{data_json['id_card_number']}',name='{data_json['name']}'," \
                  f"last_name='{data_json['last_name']}',tel='{data_json['tel']}' " \
                  f"WHERE id={data_json['id']}"
            print(sql)
            self.cursor.execute(sql)
            self.connect.commit()
            self.set_result(STATUS_SUCCESS, data_json)
            return self.result
        except db.Error as ex:
            self.set_result(STATUS_ERROR, f"Error => {ex}")
            return self.result

    def delete_tenantRoom(self, data_target):
        try:
            data_json = json.loads(data_target)
            # Update Status Room Empty
            self.update_status_room(data_json['room_number'], False)
            # Delete data byId
            delete_sql = f"DELETE FROM Tenant_registration WHERE id = {data_json['id']} "
            self.cursor.execute(delete_sql)
            self.connect.commit()

            if self.cursor.rowcount > 0:
                self.set_result(STATUS_SUCCESS)
            else:
                self.set_result(STATUS_ERROR)

            return self.result
        except db.Error as ex:
            return self.set_result(STATUS_ERROR, f"Error => {ex}")

    def update_status_room(self, room_number, status):
        try:
            update_query = f"UPDATE status_room SET status = '{status}' WHERE id = {room_number}"
            self.cursor.execute(update_query)
            self.connect.commit()
        except db.Error as ex:
            self.set_result(STATUS_ERROR, f"Error => {ex} ")

    def find_data_byId(self, id_room_number):
        try:
            query_find = f"SELECT * FROM Tenant_registration WHERE room_number = '{id_room_number}' "
            self.cursor.execute(query_find)
            result = self.cursor.fetchall()
            if len(result) > 0:
                rows_json = self.data_list_to_json(result)
                self.set_result(STATUS_SUCCESS, rows_json)
            else:
                self.set_result(STATUS_EMPTY, result)
            return self.result
        except db.Error as ex:
            self.set_result(STATUS_ERROR, f"Error => {ex}")
            return self.result

    def save_img(self, table_name, dataTarget):
        try:
            # convert String to Json
            json_datas = json.loads(dataTarget)

            json_datas['id_tenant_registration'] = self.find_tenant_by_roomnumber(
                json_datas['room_number']
            )

            Query_insert = f"INSERT INTO {table_name} (room_number,piture,unit_present,id_tenant_registration) " \
                f"VALUES('{json_datas['room_number']}','{json_datas['piture']}', '{json_datas['unit_present']}'," \
                f"'{json_datas['id_tenant_registration']}')"

            # cursor query
            self.cursor.execute(Query_insert)

            # connect commit
            self.connect.commit()

            self.set_result(STATUS_SUCCESS)
            return self.result
        except db.Error as ex:
            self.set_result(STATUS_ERROR, f"Error => {ex}")
            return self.result

    def find_dataImg_byRoomnumber(self, room_number):
        try:
            Query = f'SELECT * FROM camera_capture_unit WHERE room_number = {room_number}'

            self.cursor.execute(Query)

            data_list = self.cursor.fetchall()

            data_json = []
            if len(data_list) > 0:
                # data list to json
                data_json = self.data_list_to_json(data_list)[0]
                self.set_result(STATUS_SUCCESS, data_json)
            else:
                self.set_result(STATUS_EMPTY)

            return self.result
        except db.Error as ex:
            self.set_result(STATUS_ERROR, f"Error => {ex}")
            return self.result

    def find_tenant_by_roomnumber(self, id_roomnumber):
        query = f"SELECT id FROM Tenant_registration WHERE room_number = '{id_roomnumber}' "
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    def find_all(self, table_name):
        try:
            query_all = f"SELECT * FROM {table_name}"
            self.cursor.execute(query_all)
            data_all = self.cursor.fetchall()
            rows = self.data_list_to_json(data_all)
            return rows
        except db.Error as ex:
            self.set_result(STATUS_ERROR, f"Error => {ex} ")
            return self.result

    def convertMD5(self, password):
        return hashlib.md5(password.encode()).hexdigest()

    def set_result(self, status='', result=None):
        self.result['status'] = status
        self.result['result'] = result
        print(self.result)

    def data_list_to_json(self, data_lists):
        # Convert List to json
        rows = []
        for data_row in data_lists:
            row_dict = {}
            # ดึง Colum name ที่ได้จาก Table
            for index, colum in enumerate(self.cursor.description):
                row_dict[colum[0]] = data_row[index]
            rows.append(row_dict)

        return rows
