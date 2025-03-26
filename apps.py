from flask import Flask, render_template,request
import crwal
from send_mail_smtp import sendmail
from ticket_crwal import get_data_from_yeosin
import time
import crwal_setting
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime


app = Flask(__name__)

def print_time():
    print(time.strftime('%Y.%m.%d - %H:%M:%S'))

is_crawling = False  # 크롤링 진행 상태를 나타내는 전역 변수
request_email =[]
equipment_list = [ "올리지오", "덴서티하이","덴서티", "써마지", "볼뉴머", "텐써마", "세르프"]
# equipment_list = [ "올리지오", "덴서티", "써마지",  "세르프"]
# equipment_list = ["덴서티"]


# def start_crawling():
#     start_time = time.strftime('%Y.%m.%d - %H:%M:%S')
#     print("start_time :", start_time)
    
#     crwal.gangnamunni_crawl()
#     get_data_from_yeosin(equipment_list)
    
#     end_time = time.strftime('%Y.%m.%d - %H:%M:%S') 
#     print("end time :", end_time)

# # 서버 시작시 자동으로 크롤링 시작
# @app.before_first_request
# def initialize():
#     scheduler = BackgroundScheduler(timezone='Asia/Seoul')
#     scheduler.start()
    
#     # 즉시 한번 실행
#     start_crawling()
    
#     # 매주 월요일 자정에 실행되도록 스케줄 설정  
#     scheduler.add_job(start_crawling, 'cron', day_of_week='mon')


@app.route('/')
def index():
    # 스케줄러 생성
    scheduler = BackgroundScheduler(timezone='Asia/Seoul')
    scheduler.start()
    
    def crawl_sequence():
        try:
            start_time = time.strftime('%Y.%m.%d - %H:%M:%S')
            print("start_time :", start_time)
            
            # gangnamunni 크롤링 실행 후 yeosin 크롤링 실행
            if not crwal.gangnamunni_crawl():
                print("강남언니 크롤링 중 오류 발생")
                return
                
            if not get_data_from_yeosin(equipment_list):
                print("여신 크롤링 중 오류 발생") 
                return
            
            end_time = time.strftime('%Y.%m.%d - %H:%M:%S')
            print("end_time :", end_time)
            
        except Exception as e:
            print(f"크롤링 중 예외 발생: {e}")
            return
    
    # 매주 월요일 자정에 순차적으로 실행되도록 스케줄 설정  
    scheduler.add_job(crawl_sequence, 'cron', day_of_week='mon')
    
    # 초기 실행
    crawl_sequence()
    
    return render_template('test.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')

    
