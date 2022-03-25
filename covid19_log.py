'''
   用來設定Covid19資料分析專案記錄檔之方法
'''

import logging
import os
from datetime import datetime

#建立Covid19log類別
class Covid19log:


    def __init__(self,logs_floder):
        # 設定log檔的檔案位置
        self.dir_path = 'D:\\Cody\\covid-19\\'
        # logs_floder為log檔的資料夾
        self.logs_folder = logs_floder
        # 建立log檔資料夾，若不存在則重新建立
        if not os.path.exists(self.dir_path+"\\"+self.logs_folder):
            os.mkdir(self.dir_path+"\\"+self.logs_folder)
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s') #logger的訊息設定
        logging.captureWarnings(True)  # 捕捉Python的警告資訊
        self.logger = logging.getLogger("py.warnings") #捕捉Pyhton的警告資訊
        self.logger.setLevel(logging.INFO) #設定記錄檔顯示的最高層級

        #如logger.handlers為空則建立，反之則直接進行紀錄
        if not self.logger.handlers:
            #consolehandler 將log資訊輸出到console
            self.consoleHandler = logging.StreamHandler()
            self.consoleHandler.setLevel(logging.INFO)
            self.consoleHandler.setFormatter(self.formatter)
            self.logger.addHandler(self.consoleHandler)
            #filehandler 將log資訊輸出到日誌檔
            self.logfilename = datetime.now().strftime("%Y-%m-%d_%H_%M_%S.log")
            self.fileHandler = logging.FileHandler(self.dir_path+self.logs_folder+"/"+self.logfilename,"w","utf-8")
            self.fileHandler.setLevel(logging.INFO)
            self.fileHandler.setFormatter(self.formatter)
            self.logger.addHandler(self.fileHandler)


    #以下為各個級別資訊的方法
    def debug(self,msg):
        self.logger.debug(msg)

    def info(self,msg):
        self.logger.info(msg)

    def warning(self,msg):
        self.logger.warning(msg)

    def error(self,msg):
        self.logger.error(msg)

    def critical(self,msg):
        self.logger.critical(msg)



















