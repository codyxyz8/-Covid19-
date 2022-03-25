'''
    主執行檔，可執行Covid19的定時排程或SQL資料查詢
'''

from covid19_schedule import Covid19Schedule
from covid_pymssql_table import Covid19


# 建立Covid19排程之物件
Covid19_Main = Covid19Schedule()
# 執行Covid19定時排程
Covid19_Main.schedule()



#查詢資料範例
#如要使用請先註解掉Coivd19_Main區塊的程式碼
Covid19_Search = Covid19()
Covid19_Search.mssql_covid19_connent()
Covid19_Search.select_covid19_table()



