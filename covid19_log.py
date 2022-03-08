'''
   用來設定紀錄python專案的方法

'''

import logging
import os
from datetime import datetime

class Covid19log:

    def __init__(self,logs_floder):
        self.dir_path = 'D:\\Cody\\covid-19\\'  # 設定log檔的檔案位置
        self.logs_folder = logs_floder
        # 建立log檔資料夾，若不存在則重新建立
        if not os.path.exists(self.dir_path+"\\"+self.logs_folder):
            os.mkdir(self.dir_path+"\\"+self.logs_folder)

        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        logging.captureWarnings(True)  # 捕捉Python的警告資訊
        self.logger = logging.getLogger("py.warnings") #捕捉Pyhton的警告資訊
        self.logger.setLevel(logging.INFO)



    def consolehandler(self):
        #console handler 將log資訊輸出到console
        self.consoleHandler = logging.StreamHandler()
        self.consoleHandler.setLevel(logging.INFO)
        self.consoleHandler.setFormatter(self.formatter)
        self.logger.addHandler(self.consoleHandler)

    def filehandler(self):
        #file handler 將log資訊輸出到日誌檔
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

    #停止log檔輸入
    def close(self):
        self.logger.removeHandler(self.consoleHandler)
        self.logger.removeHandler(self.fileHandler)
        self.consoleHandler.flush()
        self.fileHandler.flush()
        self.consoleHandler.close()
        self.fileHandler.close()


















