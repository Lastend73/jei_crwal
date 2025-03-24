from flask import Flask, render_template,request
import crwal
from send_mail_smtp import sendmail
from ticket_crwal import get_data_from_yeosin
import time
import crwal_setting
5

is_crawling = False  # 크롤링 진행 상태를 나타내는 전역 변수
request_email =[]
equipment_list = [ "올리지오", "덴서티", "써마지", "볼뉴머", "텐써마", "세르프","리니어지","울쎄라","슈링크","텐쎄라","리프테라2"]
# equipment_list = [ "올리지오", "덴서티", "써마지",  "세르프"]
# equipment_list = ["덴서티"]



# request_email.append(email)
start_time = time.strftime('%Y.%m.%d - %H:%M:%S')
a = crwal.gangnamunni_crawl()
b = get_data_from_yeosin(equipment_list)
end_time = time.strftime('%Y.%m.%d - %H:%M:%S')
print("start_time :",start_time)
print("end time :",end_time)
# a.extend(b)

# crwal_setting.make_to_csv(b)

crwal_setting.quitvpn()



    
