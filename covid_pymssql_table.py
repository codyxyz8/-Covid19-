'''
    主執行程式區域。執行下載covid19Api資料
'''
import pymssql

import covid19_Source
import env
from covid19_log import Covid19log

#把下載資料傳輸到MSSQL建立資料表

class Covid19:

    def __init__(self):
        #建立covid19_log物件，執行記錄檔撰寫
        self.covid19_Log = Covid19log("covid19_Log")

    def Covid19_Data(self):
        self.covid19_Source = covid19_Source.covid19Source()
        self.covid19_Data = self.covid19_Source.Download_covid19_data()


    def MSSQL_Covid19_Connent(self):
        #運用pymmsql的函式與MSSQL連接
        import pymssql

        #引用env檔帶入pymmsql所需的敏感資訊
        server = env.server
        username = env.username
        password = env.password
        database = env.database



        #與MSSQL連接的錯誤與例外處理

        try:
            self.conn = pymssql.connect(server,username,password,database)
            self.covid19_Log.info("連接成功!!!")
            self.cursor = self.conn.cursor(as_dict=True)
        except pymssql.InterfaceError:
            self.covid19_Log.debug("連接失敗，出現MSSQL連接的問題!!!")
        except pymssql.DatabaseError:
            self.covid19_Log.debug("連接失敗，出現資料庫(DB)連接的問題")


    def Create_Covid19_Table(self):
        conn,cursor = self.conn,self.cursor
        #建立資料表的除錯與例外處理
        try:
            #判斷Covid19有沒有建立，如果有的話就Drop掉(由於本資料庫並無識別碼，為了識別碼一致採用Drop方法來處理)
            cursor.execute("""
            IF OBJECT_ID('COVID19','U') IS NOT NULL
                DROP TABLE [COVID19]""")
            #儲存變更
            conn.commit()
            #宣告command變數並定義欄位變數
            cursor.execute("""
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
            #儲存變更
            conn.commit()
            self.covid19_Log.info("成功建立Covid19資料庫之變數!!!")
        except pymssql.OperationalError:
            self.covid19_Log.debug("系統發生錯誤!!!")
        except pymssql.InternalError:
            self.covid19_Log.error("cursor未能順利執行!!!")
        except pymssql.ProgrammingError:
            self.covid19_Log.error("SQL語法錯誤!!!")

        #輸入API資料至資料表的除錯與例外處理
        try:
            #把Covid19資料匯入MSSQL資料庫裡面
            for data in self.covid19_Data:
                cursor.execute(
                    "INSERT INTO [COVID19](確定病名,個案研判日,縣市,鄉鎮,性別,境外移入與否,年齡層_以五歲為區間,確定病例數)VALUES(%s,%s,%s,%s,%s,%s,%s,%d)",
                    (data["確定病名"],data["個案研判日"],data["縣市"],data["鄉鎮"],data["性別"],data["是否為境外移入"],data["年齡層"],data["確定病例數"]))
            #儲存變更
            self.covid19_Log.info(f"執行成功!!!已存入{len(self.covid19_Data)}筆資料")
            conn.commit()
            conn.close()
        except pymssql.OperationalError:
            self.covid19_Log.debug("系統發生錯誤!!!")
        except pymssql.IntegrityError:
            self.covid19_Log.debug("資料表建置出現問題!!!")
        except pymssql.InternalError:
            self.covid19_Log.error("cursor未能順利執行!!!")
        except pymssql.ProgrammingError:
            self.covid19_Log.error("SQL語法錯誤!!!")


    def Select_Covid19_Table(self):
        conn, cursor = self.conn, self.cursor
        #查詢Covid19資料的函式
        #除錯與例外處理
        try:
            cursor.execute("""
            SELECT * FROM [COVID19] WHERE 縣市='新北市'
            """)
            for row in cursor:
                print("識別碼:%s,個案研判日:%s,縣市:%s,鄉鎮:%s,性別:%s,年齡層_以五歲為區間:%s,確定病例數:%d"%(row['識別編號'],row['個案研判日'],row['縣市'],row['鄉鎮'],row['性別'],row['年齡層_以五歲為區間'],row['確定病例數']))
            # 關閉連線
            self.covid19_Log.info(f"查詢成功!!!共有{len(row)}筆資料")
            conn.close()
        except pymssql.DataError:
            self.covid19_Log.error("處理數據發生問題!!!")
        except pymssql.OperationalError:
            self.covid19_Log.debug("系統發生錯誤!!!")
        except pymssql.IntegrityError:
            self.covid19_Log.debug("資料表建置出現問題!!!")
        except pymssql.InternalError:
            self.covid19_Log.error("cursor未能順利執行!!!")
        except pymssql.ProgrammingError:
            self.covid19_Log.error("SQL語法錯誤!!!")











