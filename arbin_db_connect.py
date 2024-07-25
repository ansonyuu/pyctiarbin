import pyodbc
cnxn = pyodbc.connect(r'Driver=SQL Server;Server=.\SQLEXPRESS;Trusted_Connection=yes;')
cursor = cnxn.cursor()

def get_tests():
    query = f"SELECT Test_ID, Test_Name, First_Start_DateTime, Database_Name from [ArbinPro8MasterInfo].[dbo].[TestList_Table] ORDER BY Test_ID DESC"
    cursor.execute(query)
    tests = []
    for row in cursor.fetchall():
        test_id, test_name, start_time, db_name = row
        tests.append({
            "id": test_id,
            "name": test_name,
            "start_time": start_time,
            "db_name": db_name
        })
    return tests

def get_data_for_test(test):
    query = f"SELECT * FROM [{test['db_name']}].[dbo].[IV_Basic_Table] WHERE Test_Id = {test['id']} ORDER BY Date_Time ASC"
    cursor.execute(query)
    data_points = []
    for row in cursor.fetchall():
        data_points.append(row)
    return data_points

for p in get_data_for_test(get_tests()[0]):
    print(p)

cursor.close()