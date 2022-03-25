'''
    設定Covid19資料分析專案的定時排程方法
'''

from covid_pymssql_table import Covid19
#引入scheduler、datatime、time的函式，進行定時排程
import sched
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
import time
from covid19_log import Covid19log


#建立Covid19Schedule類別
class Covid19Schedule:

    def __init__(self):
        #建立covid19物件
        self.covid19_data = Covid19()
        #現在時間
        self.now_time = datetime.now()
        #建立covid19_log物件，執行記錄檔撰寫
        self.covid19_log = Covid19log("covid19_Log")
        #建立自訂的timer物件
        self.updatetime = self.timer()
        


    def timer(self):

        try:
            #預計更新的時間，預設為衛福部記者會結束後一個小時，也就是每日的下午三點定時下載
            #當日未到下午三點的時間判斷式
            if 0<self.now_time.hour <15:
                self.updatetime = datetime.strptime(str(self.now_time.year)+"-"+str(self.now_time.month)+"-"+str(self.now_time.day)+" 15:00:00","%Y-%m-%d %H:%M:%S")
            #各月份(除了二月)的時間判斷式
            elif 15<self.now_time.hour<=23 and self.now_time.month in [1,3,5,7,8,10,12]:
                if self.now_time.day<31:
                    self.updatetime =self.before_the_end_of_the_month()
                elif self.now_time.day == 31:
                    self.updatetime =self.the_end_of_the_month()

            elif 15<self.now_time.hour<=23 and self.now_time.month in [4,6,9,11] and self.now_time.day<30:
                if self.now_time.day < 30:
                    self.updatetime = self.before_the_end_of_the_month()
                elif self.now_time.day == 30:
                    self.updatetime =self.the_end_of_the_month()

            #二月的閏年判斷
            elif 15<self.now_time.hour<=23 and self.now_time.month == 2:
                if self.now_time.year%4 == 0 and self.now_time.year%100 != 0 or self.now_time.year %400 == 0:
                    if self.now_time.day<29:
                        self.updatetime = self.before_the_end_of_the_month()
                    elif self.now_time.day == 29:
                        self.updatetime = self.the_end_of_the_month()
                else:
                    if self.now_time.day<28:
                        self.updatetime = self.before_the_end_of_the_month()
                    elif self.now_time.day == 28:
                        self.updatetime = self.the_end_of_the_month()
            return self.updatetime
        except ValueError:
            self.covid19_log.error("數值錯誤!!!")
        except NameError:
            self.covid19_log.error("變數未定義!!!")
        except Exception as e:
            self.covid19_log.error("其他錯誤!!!")
            print(e)

    #未到月底的更新時間函式
    def before_the_end_of_the_month(self):
        #設定明日的更新時間
        try:
            next_day = self.now_time+timedelta(days=1)
            self.updatetime = datetime.strptime(str(next_day.year)+"-"+str(next_day.month)+"-"+str(next_day.day)+" 15:00:00","%Y-%m-%d %H:%M:%S")
            return self.updatetime
        except ValueError:
            self.covid19_log.error("數值錯誤!!!")
        except NameError:
            self.covid19_log.error("變數定義有問題!!!")
        except Exception as e:
            self.covid19_log.error("其他錯誤!!!")
            print(e)

    #到月底轉換月份的更新時間函式
    def the_end_of_the_month(self):
        #設定月初的預計更新時間
        try:
            next_day = self.now_time.replace(day=1) + relativedelta(months=1)
            self.updatetime = datetime.strptime(str(next_day.year)+"-"+str(next_day.month)+"-"+str(next_day.day)+" 15:00:00","%Y-%m-%d %H:%M:%S")
            return self.updatetime
        except ValueError:
            self.covid19_log.error("數值錯誤!!!")
        except NameError:
            self.covid19_log.error("變數定義有問題!!!")
        except Exception as e:
            self.covid19_log.error("其他錯誤!!!")
            print(e)

    #主要執行定時排程的函式
    def schedule(self):

        #除錯與例外處理
        try:
            #計算預定更新時間與現在時間的時間間隔，並換算成秒數
            self.time_interval = (self.updatetime-self.now_time).total_seconds()
            print(f"更新時間:{self.updatetime}")
            print(f"時間間隔:{self.time_interval}")

            #初始化sheduler物件
            self.s = sched.scheduler(timefunc=time.time)

            #顯示開始時間
            print(f"start time:{datetime.now()}")
            self.covid19_log.info("排程成功!!!")

            self.event1 = self.s.enter(self.time_interval, 0, Covid19.covid19_data, argument=(self.covid19_data,))
            self.event2 = self.s.enter(self.time_interval, 1, Covid19.mssql_covid19_connent, argument=(self.covid19_data,))
            self.event3 = self.s.enter(self.time_interval, 2, Covid19.create_covid19_table, argument=(self.covid19_data,))
            self.s.run()
            #顯示結束時間
            print(f"end time:{datetime.now()}")
            self.covid19_log.info("執行完畢!!!")
        except ValueError:
            self.covid19_log.error("數值錯誤!!!")
        except NameError:
            self.covid19_log.error("變數定義有問題!!!")
        except Exception as e:
            self.covid19_log.error("其他錯誤!!!")
            print(e)



