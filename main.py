'''
    主執行程式區域。執行下載covid19Api資料
'''
import covid19_Source

if __name__ == "__main__":
    covid19_Data = covid19_Source.Download_covid19_data()

#把下載資料傳輸到MSSQL建立資料表

#用來連接MSSQL的方法
def MSSQL_CONNENT():

    import pymssql

    server = "127.0.0.1"
    username = "sa"
    password = "9487"
    database = "testDB101"


    try:
        conn = pymssql.connect(server,username,password,database)
        print("連接成功!!")
        cursor = conn.cursor()
        return cursor,conn
    except Exception as ex:
        print(ex)

def MSSQL_SEARCH():
    cursor,conn = MSSQL_CONNENT()

    cursor.execute("select * from 員工資料表")
    row = cursor.fetchone()
    while row:
        print("員工ID=%d,員工姓名=%s,員工薪水=%d"%(row[0],row[1],row[2]))
        row = cursor.fetchone()

    conn.close()




def MSSQL_Covid19_Connent():
    # 運用pymmsql的函式與MSSQL連接
    import pymssql

    server = "127.0.0.1"
    username = "sa"
    password = "9487"
    database = "Covid19"

    #與MSSQL連接的錯誤與例外處理

    try:
        conn = pymssql.connect(server,username,password,database)
        print("連接成功!!!")
        cursor = conn.cursor()
        return conn,cursor
    except Exception as ex:
        print(ex)

def Create_Covid19_Table():
    conn,cursor = MSSQL_Covid19_Connent()
    #判斷Covid19有沒有建立，如果有的話就Drop掉
    #宣告command變數並定義欄位變數

    cursor.execute("""
    IF OBJECT_ID("COVID19","U") IS NOT NULL
        DROP TABLE [COVID19]
    CREATE TABLE [COVID19](
    識別編號 INT IDENTITY(1,1) NOT NULL,
    確定病名 NVARCHAR(20),
    個案研判日 DATE,
    縣市 NVARCHAR(15),
    鄉鎮 NVARCHAR(15),
    性別 NVARCHAR(5),
    境外移入與否 NVARCHAR(5),
    年齡層_以五歲為區間 NVARCHAR(10),
    確定病例數 INT,
    PRIMARY KEY(識別編號)
    ) 
    """)
    #把Covid19資料匯入MSSQL資料庫裡面
    for data in covid19_Data:
        cursor.execute(
            "INSERT INTO [COVID19](確定病名,個案研判日,縣市,鄉鎮,性別,境外移入與否,年齡層,確定病例數)VALUES(%s,%Y/%m/%d,%s,%s,%s,%s,%s,%d)",
            (data["確定病名"],data["個案研判日"],data["縣市"],data["鄉鎮"],data["性別"],data["是否為境外移入"],data["年齡層"],data["確定病例數"]))
    #儲存變更
    conn.commit()
    #關閉連線
    conn.close()

Create_Covid19_Table()









