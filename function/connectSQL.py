import pyodbc as db


class SQL:
    connect = None
    cursor = None

    def __init__(self, server_name, database_name):
        # connect to database
        self.connect_database(server_name, database_name)

    def connect_database(self, server_name, database_name):
        try:
            self.connect = db.connect(
                "Driver={SQL Server};"
                f"Server={server_name};"
                f"Database={database_name};"
                "Trusted_Connection=yes;")

            # connect to cuesor
            self.cursor = self.connect.cursor()

        except db.Error as ex:
            print('Error connecting to : ', ex)

    def select_query(self, table_name):
        try:
            query = f'SELECT * FROM {table_name}'
            self.cursor.execute(query)

            # Check result
            for row in self.cursor:
                print(row)

        except db.Error as ex:
            print('Error Select table : ', ex)

    def insert_data(self, table_name, list_values):
        try:
            # print('Data List => ', list_values)
            insert_data = f'INSERT INTO {table_name} (name,age) VALUES {list_values}'
            # insert_data = f"INSERT INTO {table_name} (name,age) VALUES ('019854\n',10)"

            # excute query
            self.cursor.execute(insert_data)

            # เปลี่ยนแปลงข้อมูล
            self.connect.commit()

            # ปิดการเชิ่มต่อ
            self.connect.close()

        except db.Error as ex:
            print('Error => ', ex)
