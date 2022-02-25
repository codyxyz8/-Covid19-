'''
    從政府開放平台下載台灣covid-19各地區年齡性別統計表-依個案研判日統計。並解析Json檔
    :return latestfile
'''

__all__ = ["Download_covid19_data"] #可開放的屬性、類別與方法

#-----------下載資料開始--------------#
import json


def Download_covid19_data():
    import requests
    from requests.exceptions import HTTPError
    url = "https://od.cdc.gov.tw/eic/Day_Confirmation_Age_County_Gender_19CoV.json"
    #除錯與例外處理
    try:
        response = requests.get(url)
        response.raise_for_status()
    except ConnectionError as e:
        raise ValueError("連線錯誤!!")
    except HTTPError as e:
        raise ValueError("HTTP錯誤!!")
    except requests.Timeout as e:
        raise ValueError("連線過長!!")
    except Exception:
        raise ValueError("其他錯誤!!")

#---------下載資料結束--------#

#---------總執行流程開始------#
    savefile(response.text) #儲存從api下載的covid-19資料
    latestfile = Get_Lastfile_Path() #取得最新的json檔路徑
    #開啟最新的covid19資料的json檔
    covid19_lastestfile = open(latestfile,"r",encoding="utf-8")
    #將json檔轉換成python的字典格式並關檔
    covid19_jsonfile = json.load(covid19_lastestfile)
    covid19_lastestfile.close()
    #回傳python list物件
    return covid19_jsonfile

#---------總執行流程結束------#

#---------儲存資料開始--------#
'''
    用當前時間來儲存json檔
'''

def savefile(apitext):
    import os
    from datetime import datetime
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
    file.write(apitext)
    file.close()
#---------儲存資料結束--------#

#---------取出最新資料檔開始-----#

def Get_Lastfile_Path():
    '''
    從covid19_DataFolder取出最新下載資料的絕對路徑
    :return:lastestfilepath
    '''
    import os
    foldername = "covid19_DataFolder"
    filenames = os.listdir(foldername)

    #新增list來存放所有json檔案，並取出最新的json檔
    filelist = []
    for filename in filenames:
        filelist.append(filename)
    filelist.sort()
    lastestfilepath = os.path.abspath(f"{foldername}/{filelist[-1]}")
    return lastestfilepath

#---------取出最新資料檔結束-----#

