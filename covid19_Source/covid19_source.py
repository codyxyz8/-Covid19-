'''
    從政府開放平台下載台灣covid-19各地區年齡性別統計表-依個案研判日統計。並儲存成Json檔傳出
    :return covid19_jsonfile
'''

__all__ = ["Covid19Source"] #可開放的屬性、類別與方法


import json
from covid19_log import Covid19log



#建立Covid19Source類別
class Covid19Source:

    # -----------下載資料開始--------------#
    def __init__(self):
        #covid19資料 API網址
        self.url = "https://od.cdc.gov.tw/eic/Day_Confirmation_Age_County_Gender_19CoV.json"
        #建立covid19log物件，執行記錄檔撰寫
        self.covid19_log = Covid19log("covid19_Log")

    def download_covid19_data(self):
        import requests
        from requests.exceptions import HTTPError
        #除錯與例外處理
        try:
            #使用requests進行API資料下載
            self.response = requests.get(self.url)
            self.response.raise_for_status()
            self.covid19_log.info("下載成功!!!")
        except ConnectionError:
            self.covid19_log.error("連線錯誤!!")
        except HTTPError:
            self.covid19_log.error("HTTP錯誤!!")
        except requests.Timeout:
            self.covid19_log.error("連線過長!!")
        except Exception:
            self.covid19_log.error("其他錯誤!!")

    #---------下載資料結束--------#

    #---------總執行流程開始------#
        self.savefile(self.response.text) #儲存從api下載的covid19資料
        latestfile = self.get_lastfile_path() #取得最新的json檔路徑
        #開啟最新的covid19資料的json檔
        covid19_lastestfile = open(latestfile,"r",encoding="utf-8")
        #將json檔轉換成python的字典格式並關檔
        covid19_jsonfile = json.load(covid19_lastestfile)
        covid19_lastestfile.close()
        #回傳python list物件
        return covid19_jsonfile

    #---------總執行流程結束------#

    #---------儲存資料開始--------#

    def savefile(self, response):

        #以當前時間儲存json檔

        import os
        from datetime import datetime
        #除錯與例外處理
        try:
            foldername = "covid19_DataFolder" #資料夾名稱
            now = datetime.now() #當前時間
            filename = f"{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}.json" #json檔存檔名稱
            savepath = f"./{foldername}/{filename}" #存檔絕對路徑
            abspath = os.path.abspath(savepath) #返回絕對路徑
            # 檢查資料夾有沒有存在，不存在就新增一個
            if not os.path.exists(foldername):
                os.mkdir(foldername)
            # 儲存成json檔案
            file = open(abspath,"w",encoding="utf-8")
            file.write(response)
            file.close()
            self.covid19_log.info("json檔儲存成功!!!")
        except ValueError:
            self.covid19_log.error("數值錯誤!!!")
        except FileNotFoundError:
            self.covid19_log.error("資料夾不存在!!!")
        except NameError:
            self.covid19_log.error("變數名稱有問題!!!")
        except Exception as e:
            self.covid19_log.error("其他錯誤!!!")
            print(e)


    #---------儲存資料結束--------#

    #---------取出最新資料檔開始-----#

    def get_lastfile_path(self):

        #從covid19_DataFolder取出最新下載資料的絕對路徑
        #return:lastestfilepath

        import os
        from datetime import datetime
        foldername = "covid19_DataFolder"
        filenames = os.listdir(foldername)

        #除錯與例外處理
        try:
            #建立datetimelist變數將檔案路徑轉成datetime物件
            datetimelist = [datetime.strptime(filename,"%Y-%m-%d-%H-%M-%S.json") for filename in filenames]
            #把list由小到大排列，並抓取串列最後一筆資料，也就是最新檔案路徑
            datetimelist.sort()
            lasttimefile = datetimelist[-1]
            #將datetime物件變為字串
            lasttimefilename = f"{lasttimefile.year}-{lasttimefile.month}-{lasttimefile.day}-{lasttimefile.hour}-{lasttimefile.minute}-{lasttimefile.second}.json"
            #再轉為絕對路徑輸出
            lastestfilepath = os.path.abspath(f"{foldername}/{lasttimefilename}")
            self.covid19_log.info("成功回傳最新json檔路徑")
            return lastestfilepath
        except ValueError:
            self.covid19_log.error("數值錯誤!!!")
        except FileNotFoundError:
            self.covid19_log.error("資料夾不存在!!!")
        except NameError:
            self.covid19_log.error("變數名稱有問題!!!")
        except Exception as e:
            self.covid19_log.error("其他錯誤!!!")
            print(e)


    #---------取出最新資料檔結束-----#

