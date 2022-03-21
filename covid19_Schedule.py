from covid_pymssql_table import Covid19

#引入scheduler、datatime、time的函式，進行定時排程
import sched
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
import time
from covid19_log import Covid19log



class Covid19Schedule:

    def __init__(self):
        #建立covid19物件
        self.covid19_data = Covid19()
        #現在時間
        self.now_time = datetime.now()
        #建立covid19_log物件，執行記錄檔撰寫
        self.covid19_Log = Covid19log("covid19_Log")
        #建立自訂的timer物件
        self.updatetime = self.timer()
        


    def timer(self):

        try:
            #預計更新的時間，預設為衛福部記者會結束後一個小時，也就是每日的下午三點定時下載
            #當日未到下午三點的時間判斷式
            if 0<self.now_time.hour <15:
                self.updatetime = datetime.strptime(str(self.now_time.year)+"-"+str(self.now_time.month)+"-"+str(self.now_time.day)+" 12:55:00","%Y-%m-%d %H:%M:%S")
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
            self.covid19_Log.error("數值錯誤!!!")
        except NameError:
            self.covid19_Log.error("變數未定義!!!")
        except Exception:
            self.covid19_Log.error("其他錯誤!!!")
    #未到月底的更新時間函數
    def before_the_end_of_the_month(self):
        #設定明日的更新時間
        try:
            next_day = self.now_time+timedelta(days=1)
            self.updatetime = datetime.strptime(str(next_day.year)+"-"+str(next_day.month)+"-"+str(next_day.day)+" 15:00:00","%Y-%m-%d %H:%M:%S")
            return self.updatetime
        except ValueError:
            self.covid19_Log.error("數值錯誤!!!")
        except NameError:
            self.covid19_Log.error("變數定義有問題!!!")
        except Exception:
            self.covid19_Log.error("其他錯誤!!!")

    #到月底轉換月份的更新時間函數
    def the_end_of_the_month(self):
        #設定月初的預計更新時間
        try:
            next_day = self.now_time.replace(day=1) + relativedelta(months=1)
            self.updatetime = datetime.strptime(str(next_day.year)+"-"+str(next_day.month)+"-"+str(next_day.day)+" 15:00:00","%Y-%m-%d %H:%M:%S")
            return self.updatetime
        except ValueError:
            self.covid19_Log.error("數值錯誤!!!")
        except NameError:
            self.covid19_Log.error("變數定義有問題!!!")
        except Exception:
            self.covid19_Log.error("其他錯誤!!!")

    def schedule(self):

        try:
            #計算預定更新時間與現在時間的時間間隔，並換算成秒數
            self.time_interval = (self.updatetime-self.now_time).total_seconds()
            print(f"更新時間:{self.updatetime}")
            print(f"時間間隔:{self.time_interval}")

            #初始化sheduler
            self.s = sched.scheduler(timefunc=time.time)

            print(f"start time:{datetime.now()}")
            self.covid19_Log.info("排程成功!!!")

            self.event1 = self.s.enter(self.time_interval,0,Covid19.Covid19_Data,argument=(self.covid19_data,))
            self.event2 = self.s.enter(self.time_interval,1,Covid19.MSSQL_Covid19_Connent,argument=(self.covid19_data,))
            self.event3 = self.s.enter(self.time_interval,2,Covid19.Create_Covid19_Table,argument=(self.covid19_data,))
            self.s.run()
            print(f"end time:{datetime.now()}")
            self.covid19_Log.info("執行完畢!!!")
        except ValueError:
            self.covid19_Log.error("數值錯誤!!!")
        except NameError:
            self.covid19_Log.error("變數定義有問題!!!")
        except Exception as e:
            self.covid19_Log.error("其他錯誤!!!")
            print(e)
        # 關閉記錄檔
        finally:
            self.covid19_Log.close()

    def sche_cancel(self):
        #取消排程的函式
        try:
            self.s.cancel(self.event1)
            self.s.cancel(self.event2)
            self.s.cancel(self.event3)
        except ValueError:
            self.covid19_Log.error("數值錯誤!!!")
        except NameError:
            self.covid19_Log.error("變數定義有問題!!!")
        except Exception:
            self.covid19_Log.error("其他錯誤!!!")




