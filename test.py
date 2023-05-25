from sqlalchemy import insert, Table, Column, Integer, String, MetaData, update, delete
import sqlalchemy
from sqlalchemy.orm import sessionmaker, declarative_base

metadata = MetaData()

connect = "Driver={ODBC Driver 17 for SQL Server};" \
          "Server=DESKTOP-R4AEEG6\SQLEXPRESS;" \
          "Database=testDatabase;" \
          "Trusted_Connection=yes;"

# สร้าง SQLAlchemy engine
engine = sqlalchemy.create_engine('mssql+pyodbc:///?odbc_connect=' + connect)

# สร้าง Session
Session = sessionmaker(bind=engine)
session = Session()

# สร้าง BaseModel
Base = declarative_base()


# สร้างโมเดล (Model) สำหรับตารางในฐานข้อมูล
class infoMitor(Base):
    __tablename__ = 'info_mitor'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)


data_json = {
    'id': None,
    'name': 'Test 4',
    'age': '456'
}
id = 1

# สร้างข้อมูลและทำการ Insert
# new_data = infoMitor(**data_json)
# session.add(new_data)
# session.commit()

# Select ข้อมูลทั้งหมด
# dataRow = session.query(infoMitor).all()
# result = [row.__dict__ for row in dataRow]

# Select ข้อมูลตามเงี่อนไข
# dataRow = session.query(infoMitor).filter_by(id=12)
# result = [row.__dict__ for row in dataRow]

# data_json = [{key: value for key, value in row.items() if key != '_sa_instance_state'} for row in result]
# print(data_json)

# สร้างคำสั่ง SQL UPDATE
# session.query(infoMitor).filter_by(id=id).update(data_json)
# session.commit()
# stmt = update(table).values(**data_json).where(table.c.id == id_)

# Delete ข้อมูล
# data_delete = session.query(infoMitor).filter_by(id=1).first()
# session.delete(data_delete)
# session.commit()

# ปิด Session
session.close()
