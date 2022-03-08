'''
    主執行檔，可執行Covid19的定時排程
'''

from covid19_Schedule import Covid19Schedule

#建立Covid19排程的物件
Covid19_Main = Covid19Schedule()
Covid19_Main.schedule()

