from function.dataStatic import *
import pyodbc as db
import hashlib
import json

from sqlalchemy import insert, Table, Column, Integer, String, MetaData, update, delete, and_, Float, desc
import sqlalchemy
from sqlalchemy.orm import sessionmaker, declarative_base


# -------------------------------- Function --------------------------------
def convertMD5(password):
    return hashlib.md5(password.encode()).hexdigest()


def convert_to_json(data_all):
    # Convert to json
    data_json = []
    if data_all:
        result = [row.__dict__ for row in data_all]
        data_json = [{key: value for key, value in row.items() if key != '_sa_instance_state'} for row in result]

    return data_json


# -------------------------------- End Function --------------------------------

class SQL:
    serverName = ''
    databaseName = ''
    session = None
    Base = declarative_base()  # สร้าง BaseModel

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

            # self.connect = db.connect(
            #     'Driver={ODBC Driver 17 for SQL Server};'
            #     f'Server={self.serverName};Database={self.databaseName};UID=sqlserver;PWD=~|YQ4p->-vv*dk\P'
            # )
            connect = 'Driver={ODBC Driver 17 for SQL Server};' \
                      f'Server={self.serverName};Database={self.databaseName};UID=sqlserver;PWD=~|YQ4p->-vv*dk\P'

            # สร้าง SQLAlchemy engine
            engine = sqlalchemy.create_engine('mssql+pyodbc:///?odbc_connect=' + connect)

            # สร้าง Session
            Session = sessionmaker(bind=engine)
            self.session = Session()

            # connect to cuesor
            # self.cursor = self.connect.cursor()

            return set_result(STATUS_SUCCESS, 'Connect Suscess')

        except sqlalchemy.exc.InterfaceError as ex:
            print('Error connecting to : ', ex)
            return set_result(STATUS_ERROR, f'Error connecting to : {ex}')

    def findUserPassByAdminPass(self, admin_pass):
        try:
            self.connect_database()

            # query = f"SELECT id_admin,username FROM host WHERE admin_password = '{admin_pass}' "
            # self.cursor.execute(query)
            # data_list = self.cursor.fetchall()

            dataRow = self.session.query(self.Host).filter_by(
                admin_password=admin_pass).all()
            self.session.close()

            if dataRow:
                result = [row.__dict__ for row in dataRow]
                data_json = [
                    {key: value for key, value in row.items() if key != '_sa_instance_state'} for row in result][0]
                data_dict = {
                    'id_admin': data_json['id_admin'],
                    'username': data_json['username']
                }
                return set_result(STATUS_SUCCESS, data_dict)
            else:
                return set_result(STATUS_EMPTY, 'ไม่พบข้อมูล')
        except sqlalchemy.exc.InterfaceError as ex:
            print('Error Select table : ', ex)
            return set_result(STATUS_ERROR, f'Error Select table : {ex}')

    def check_login(self, user, password):
        try:
            self.connect_database()

            # convert md5
            MD5Password = convertMD5(password)

            # query = f"SELECT * FROM host WHERE username = '{user}' AND password = '{MD5Password}' "
            dataRow = self.session.query(self.Host).filter(
                and_(self.Host.username == user, self.Host.password == MD5Password)).all()

            self.session.close()

            if dataRow:
                # result = [row.__dict__ for row in dataRow]
                # data_json = [
                #     {key: value for key, value in row.items() if key != '_sa_instance_state'} for row in result
                # ]
                # data_json = convert_to_json(dataRow)[0]
                # data = data_json[0] if len(data_json) == 1 else data_json
                return set_result(STATUS_SUCCESS)
            else:
                return set_result(STATUS_EMPTY)
        except sqlalchemy.exc.InterfaceError as ex:
            print(f'Error => {ex}')
            return set_result(STATUS_ERROR, f'Error => {ex}')

    def change_password(self, new_password, id_admin):
        try:
            self.connect_database()

            pass_md5 = convertMD5(new_password)
            self.session.query(self.Host).filter_by(id_admin=id_admin).update({'password': pass_md5})
            self.session.commit()

            self.session.close()
            # query_change = f"UPDATE host SET password = '{pass_md5}' WHERE id_admin = {id_admin} "
            # self.cursor.execute(query_change)
            # self.connect.commit()

            # self.cursor.close()
            # self.connect.close()

            # set status
            return set_result(STATUS_SUCCESS)
        except sqlalchemy.exc.InterfaceError as ex:
            return set_result(STATUS_ERROR, f'Error => {ex}')

    def insert_data(self, table_name, dataTarget):
        try:
            # open
            self.connect_database()

            # convert String to Json
            json_datas = json.loads(dataTarget)

            if table_name == "host":
                # convert password MD5
                json_datas['password'] = convertMD5(
                    json_datas['password'])

                # print(json_datas)
                # สร้างข้อมูลและทำการ Insert
                new_data = self.Host(**json_datas)
                self.session.add(new_data)
                self.session.commit()

            elif table_name == 'Tenant_registration':
                # update status room tenant
                self.update_status_room(json_datas['room_number'], True)
                new_data = self.tenantRegistration(**json_datas)
                self.session.add(new_data)
                self.session.commit()

            elif table_name == 'calculate_unit':
                # print(json_datas)
                new_data = self.calculateUnit(**json_datas)
                self.session.add(new_data)
                self.session.commit()

            # print(json_datas)
            # # สร้างข้อมูลและทำการ Insert
            # new_data = self.Host(**json_datas)
            # self.session.add(new_data)
            # self.session.commit()

            # [json_datas[field] for field in json_datas if field != 'id_admin']
            # value_list = [json_datas[field] for field in json_datas]

            # print(value_list)
            # convert List to String
            # value_list_toStr = ','.join(
            #     [elem if type(elem) == int else f'\'{elem}\'' for elem in value_list])
            # value_list_toStr = ','.join([elem for elem in value_list])

            # Query insert
            # insert_data = f"INSERT INTO {table_name} VALUES ({value_list_toStr}) "

            # excute query
            # self.cursor.execute(insert_data)

            # เปลี่ยนแปลงข้อมูล
            # self.connect.commit()

            # ปิดการเชิ่มต่อ
            # self.cursor.close()
            # self.connect.close()
            self.session.close()

            return set_result(STATUS_SUCCESS)
        except sqlalchemy.exc.InterfaceError as ex:
            print('Error => ', ex)
            return set_result(STATUS_ERROR, f'Error => {ex}')

    def update_call(self, table_name, dataTarget):
        try:
            # open
            self.connect_database()

            # convert String to Json
            json_datas = json.loads(dataTarget)

            if table_name == 'calculate_unit':
                new_data_update = {
                    row: json_datas[row] for row in json_datas if row not in ['id', 'date_call', 'time_call']
                }
                id_call = json_datas['id']
                self.session.query(self.calculateUnit).filter_by(id=id_call).update(new_data_update)
                self.session.commit()
            # Query = f"UPDATE {table_name} " \
            #         f"SET unit_before = {json_datas['unit_before']},unit_used = {json_datas['unit_used']}," \
            #         f"electricity_rate = {json_datas['electricity_rate']}, electricity_bill = {json_datas['electricity_bill']}," \
            #         f"room_rental = {json_datas['room_rental']},Other = {json_datas['Other']},Total = {json_datas['Total']}," \
            #         f"room_number =  '{json_datas['room_number']}',unit_present = {json_datas['unit_present']} " \
            #         f"WHERE id = {json_datas['id']} "
            # self.cursor.execute(Query)
            #
            # self.cursor.commit()
            #
            # self.cursor.close()
            #
            # self.connect.close()

            self.session.close()
            return set_result(STATUS_SUCCESS)
        except sqlalchemy.exc.InterfaceError as ex:
            return set_result(STATUS_ERROR, ex)

    def edit_tenantRoom(self, data_edit):
        try:
            self.connect_database()

            data_json = json.loads(data_edit)
            # print(data_json)
            # sql = "UPDATE Tenant_registration " \
            #       f"SET room_number='{data_json['room_number']}',chek_in='{data_json['chek_in']}',chek_out='{data_json['chek_out']}'," \
            #       f"status_date='{data_json['status_date']}',id_card_number='{data_json['id_card_number']}',name='{data_json['name']}'," \
            #       f"last_name='{data_json['last_name']}',tel='{data_json['tel']}' " \
            #       f"WHERE id={data_json['id']}"
            tenant_id = data_json['id']
            # new_data_update = [{key: value for key, value in row.items() if key != 'id'} for row in data_json]
            # print(data_json)
            new_data_update = {row: data_json[row] for row in data_json if row != 'id'}
            # print(new_data_update)
            self.session.query(self.tenantRegistration).filter_by(id=tenant_id).update(new_data_update)
            self.session.commit()
            self.session.close()
            # self.cursor.execute(sql)
            # self.connect.commit()
            #
            # self.cursor.close()
            # self.connect.close()
            return set_result(STATUS_SUCCESS, data_json)
        except sqlalchemy.exc.InterfaceError as ex:
            return set_result(STATUS_ERROR, f"Error => {ex}")

    def delete_tenantRoom(self, data_target):
        try:
            # open
            self.connect_database()

            data_json = json.loads(data_target)
            # Update Status Room Empty
            self.update_status_room(data_json['room_number'], False)
            # Delete data byId
            # delete_sql = f"DELETE FROM Tenant_registration WHERE id = {data_json['id']} "
            # self.cursor.execute(delete_sql)
            # self.connect.commit()

            tenant_id = data_json['id']
            data_delete = self.session.query(self.tenantRegistration).filter_by(id=tenant_id).first()
            # self.session.delete(data_delete)
            # self.session.commit()

            if data_delete:
                self.session.delete(data_delete)
                self.session.commit()
                self.session.close()
                return set_result(STATUS_SUCCESS)
            else:
                self.session.close()
                return set_result(STATUS_ERROR)

        except sqlalchemy.exc.InterfaceError as ex:
            return set_result(STATUS_ERROR, f"Error => {ex}")

    def update_status_room(self, room_number, status):
        try:
            # update_query = f"UPDATE status_room SET status = '{status}' WHERE id = {room_number}"
            # self.cursor.execute(update_query)
            # self.connect.commit()
            self.session.query(self.statusRoom).filter_by(id=room_number).update({'status': status})
            self.session.commit()
        except sqlalchemy.exc.InterfaceError as ex:
            print(ex)
            set_result(STATUS_ERROR, f"Error => {ex} ")

    def find_data_byId(self, id_room_number, table_name):
        try:
            # open connect database
            self.connect_database()

            dataRow = []
            if table_name == 'Tenant_registration':
                dataRow = self.session.query(self.tenantRegistration).filter_by(room_number=id_room_number).all()
                self.session.close()

            if dataRow:
                result = [row.__dict__ for row in dataRow]
                data_json = [
                    {key: value for key, value in row.items() if key != '_sa_instance_state'} for row in result]

                return set_result(STATUS_SUCCESS, data_json)
            else:
                return set_result(STATUS_EMPTY, dataRow)
            # query_find = f"SELECT * FROM {table_name} WHERE room_number = '{id_room_number}' "
            # self.cursor.execute(query_find)
            # result = self.cursor.fetchall()

            # if len(result) > 0:
            #     rows_json = self.data_list_to_json(result)
            #
            #     # Close Database
            #     self.cursor.close()
            #     self.connect.close()
            #
            #     return set_result(STATUS_SUCCESS, rows_json)
            # else:
            #     # Close Database
            #     self.cursor.close()
            #     self.connect.close()
            #
            #     return set_result(STATUS_EMPTY, result)

        except sqlalchemy.exc.InterfaceError as ex:
            return set_result(STATUS_ERROR, f"Error => {ex}")

    def save_img(self, table_name, dataTarget):
        try:
            # open
            self.connect_database()

            # convert String to Json
            json_datas = json.loads(dataTarget)

            # find id tenant registration
            json_datas['id_tenant_registration'] = self.find_tenant_by_roomnumber(
                json_datas['room_number']
            )

            # print('not null' if json_datas['id'] != None else 'null')

            if json_datas['id'] != None:  # update
                # print('update')
                camera_id = json_datas['id']
                # ไม่เอา colum Id
                data_update = {row: json_datas[row] for row in json_datas if row != 'id'}
                self.session.query(self.cameraCaptureUnit).filter_by(id=camera_id).update(data_update)
                self.session.commit()

            else:  # insert
                # print('insert')
                new_data = self.cameraCaptureUnit(**json_datas)
                self.session.add(new_data)
                self.session.commit()

            self.session.close()

            return set_result(STATUS_SUCCESS)
        except sqlalchemy.exc.InterfaceError as ex:
            return set_result(STATUS_ERROR, f"Error => {ex}")

    def find_dataImg_byRoomnumber(self, room_number):
        try:
            # open
            self.connect_database()

            data_result = self.session.query(self.cameraCaptureUnit).filter_by(room_number=room_number).all()
            if data_result:
                result = [row.__dict__ for row in data_result]
                data_json = [
                    {key: value for key, value in row.items() if key != '_sa_instance_state'} for row in result
                ]
                self.session.close()

                return set_result(STATUS_SUCCESS, data_json[0])
            else:
                #     # close
                self.session.close()
                return set_result(STATUS_EMPTY)

        except sqlalchemy.exc.InterfaceError as ex:
            return set_result(STATUS_ERROR, f"Error => {ex}")

    def find_tenant_by_roomnumber(self, id_roomnumber):
        data = self.session.query(self.tenantRegistration.id).filter_by(room_number=id_roomnumber).first()
        # print(data[0])
        # query = f"SELECT id FROM Tenant_registration WHERE room_number = '{id_roomnumber}' "
        # self.cursor.execute(query)
        return data[0]

    def find_all(self, table_name):
        try:
            # open
            self.connect_database()

            dataRow = []
            if table_name == 'status_room':
                dataRow = self.session.query(self.statusRoom).all()
            # query_all = f"SELECT * FROM {table_name}"
            # self.cursor.execute(query_all)
            # data_all = self.cursor.fetchall()
            # rows = self.data_list_to_json(data_all)
            result = [row.__dict__ for row in dataRow]
            data_json = [{key: value for key, value in row.items() if key != '_sa_instance_state'} for row in result]

            # close
            # self.cursor.close()
            # self.connect.close()
            self.session.close()

            return data_json
        except sqlalchemy.exc.InterfaceError as ex:
            return set_result(STATUS_ERROR, f"Error => {ex} ")

    def find_data_call_miter_byId(self, room_number):
        try:
            # open
            self.connect_database()

            # find table camera_capture_unit by room_number
            data_camera = self.session.query(self.cameraCaptureUnit).filter_by(room_number=room_number).all()

            # find data call miter by room_number
            data_call_miter = self.session.query(self.calculateUnit).filter_by(room_number=room_number).order_by(
                desc(self.calculateUnit.date_call), desc(self.calculateUnit.id)).all()

            # Query = f"SELECT * FROM calculate_unit WHERE room_number = '{room_number}' "
            # self.cursor.execute(Query)
            # dataRow = self.cursor.fetchall()
            # dataJson = self.data_list_to_json(dataRow)
            #
            # # close
            # self.cursor.close()
            # self.connect.cursor()
            #
            if data_camera and data_call_miter:  # not Empty all
                data_json_camera = convert_to_json(data_camera)[0]
                # print('data_json_camera :', data_json_camera['unit_present'])

                data_json_call_miter = convert_to_json(data_call_miter)[0]
                # print(data_json_call_miter['unit_present'])

                # swap unit_present to unit_before
                if data_json_call_miter['unit_present'] != data_json_camera['unit_present']:
                    data_json_call_miter['unit_before'] = data_json_call_miter['unit_present']
                    data_json_call_miter['unit_present'] = data_json_camera['unit_present']
                    data_json_call_miter['date_call'] = data_json_camera['date_call']

                    # update data
                    data_update = {k: v for k, v in data_json_call_miter.items() if k != 'id'}
                    self.session.query(self.calculateUnit).filter_by(room_number=room_number).update(data_update)
                    self.session.commit()
                    self.session.close()

                # set add Data
                data_json_call_miter['date_call'] = data_json_camera['date_call']
                data_json_call_miter['time_call'] = data_json_camera['time_call']

                return set_result(STATUS_SUCCESS, data_json_call_miter)
                # return set_result(STATUS_SUCCESS, '')
            elif not data_camera:  # camera Empty
                return set_result(STATUS_EMPTY)
            else:
                data_json_camera = convert_to_json(data_camera)[0]
                data_json_call = {
                    'unit_present': data_json_camera['unit_present'],
                    'room_number': data_json_camera['room_number'],
                    'id': None
                }
                return set_result(STATUS_SUCCESS, data_json_call)

        except sqlalchemy.exc.InterfaceError as ex:
            return set_result(STATUS_ERROR, f"Error => {ex}")

    def find_callmiter_lists_by_roomnumber(self, room_number):
        try:
            self.connect_database()
            result = self.session.query(self.calculateUnit).filter_by(room_number=room_number).all()
            result_info = self.session.query(self.tenantRegistration).filter_by(room_number=room_number).all()
            result_camera = self.session.query(self.cameraCaptureUnit).filter_by(room_number=room_number).all()
            self.session.close()
            data_json = []
            if result:
                data_json = convert_to_json(result)
                data_json_info = convert_to_json(result_info)[0]
                data_json_camear = convert_to_json(result_camera)[0]

                for data in data_json:
                    data['fullname'] = f'{data_json_info["name"]} {data_json_info["last_name"]}'
                    data['date_call'] = data_json_camear['date_call']
                    data['time_call'] = data_json_camear['time_call']

                return set_result(STATUS_SUCCESS, data_json)

            return set_result(STATUS_EMPTY, data_json)
        except sqlalchemy.exc.InterfaceError as ex:
            print(ex)
            return set_result(STATUS_ERROR, ex)

    # -------------------------- Class Method Table ---------------------------
    class Host(Base):
        __tablename__ = 'host'
        id_admin = Column(Integer, primary_key=True)
        username = Column(String)
        password = Column(String)
        admin_password = Column(String)
        name_host = Column(String)
        last_name = Column(String)
        email = Column(String)
        phone_number = Column(String)

    class statusRoom(Base):
        __tablename__ = 'status_room'
        id = Column(Integer, primary_key=True)
        room_number = Column(String)
        status = Column(Integer)

    class tenantRegistration(Base):
        __tablename__ = 'Tenant_registration'
        id = Column(Integer, primary_key=True)
        room_number = Column(String)
        chek_in = Column(String)
        chek_out = Column(String)
        status_date = Column(Integer)
        id_card_number = Column(String)
        name = Column(String)
        last_name = Column(String)
        tel = Column(String)

    class cameraCaptureUnit(Base):
        __tablename__ = 'camera_capture_unit'
        id = Column(Integer, primary_key=True)
        room_number = Column(String)
        piture = Column(String)
        unit_present = Column(Float)
        id_tenant_registration = Column(Integer)
        date_call = Column(String)
        time_call = Column(String)

    class calculateUnit(Base):
        __tablename__ = 'calculate_unit'
        id = Column(Integer, primary_key=True)
        unit_present = Column(Float)
        unit_before = Column(Float)
        unit_used = Column(Float)
        electricity_rate = Column(Float)
        electricity_bill = Column(Float)
        room_rental = Column(Float)
        Other = Column(Float)
        Total = Column(Float)
        room_number = Column(String)
        date_call = Column(String)
