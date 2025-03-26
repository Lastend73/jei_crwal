import mysql.connector
from mysql.connector import Error
import time
import re

# MySQL 접속 정보
def create_connection():
  mydb = mysql.connector.connect(
    host="192.168.0.54", # MySQL 서버 주소
    user="kyu233", # MySQL 사용자 이름
    password="min818919", # MySQL 비밀번호
    database='DB_Schema' # 접속할 데이터베이스 이름
  )

  # 접속 확인
  if not mydb.is_connected():
    print("MySQL 접속에 실패했습니다.")
  return mydb
# 데이터베이스 작업
# ...

#[병원명, 주소, 옵션명, 가격, 링크, 출처, 날짜]
def execute_query(list):
    connection = create_connection()
    cursor = connection.cursor()
    # print(list[2]) 옵션명명
    if "샷" not in list[2] :
        print("샷없음")
        return None
    if "+" in list[2] :
        print("합성")
        return None
    index = list[2].find("샷")
    print(index)
    if index != -1 :
        # 앞에 3글자 중 숫자만 추출
        if index < 4 :
            index = 4 
        shot_name = int(re.sub(r'[^0-9]', '', list[2][index-4:index]))
        print(shot_name)

    region_name = list[1].split(' ')

    if '서울' in region_name[0] :
        region_name[0] = '서울시'
    elif '경기' in region_name[0] :
        region_name[0] = '경기도'
    elif '인천' in region_name[0] :
        region_name[0] = '인천광역시'
    elif '제주' in region_name[0] :
        region_name[0] = '제주'
    elif '대전' in region_name[0] :
        region_name[0] = '대전'
    elif '부산' in region_name[0] :
        region_name[0] = '부산'
    elif '강원' in region_name[0] :
        region_name[0] = '강원도'
    elif '대구' in region_name[0] :
        region_name[0] = '대구'
    elif '광주' in region_name[0] :
        region_name[0] = '광주'
    elif '충남' in region_name[0] or '충청남도' in region_name[0]:
        region_name[0] = '충청남도'
    elif '충북' in region_name[0] or '충청북도' in region_name[0]:
        region_name[0] = '충청북도'
    elif '경남' in region_name[0] or '경상남도' in region_name[0]:
        region_name[0] = '경상남도'
    elif '경북북' in region_name[0] or '경상북도' in region_name[0]:
        region_name[0] = '경상북도'
    elif '울산' in region_name[0] :
        region_name[0] = '울산'


    region_name = region_name[0] +' ' + region_name[1]

    if '피부과' in list[0] and '강남' in list[1] :
        tier = 1
    elif ('피부과' in list[0] and ('서울' in list[0] or'경기' in list[0] or'인천' in list[0] )  ) or '강남' in list[1] :
        tier = 2
    else :
        tier = 3
    
    equipment_list = [ "올리지오X", "올리지오" , "덴서티하이", "덴서티", "써마지FLX", "볼뉴머", "텐써마", "세르프", "리니어지", "울쎄라", "슈링크", "텐쎄라", "리프테라2"]
    equipment = ''
    for equipment_info in equipment_list:
        if equipment_info in list[2].replace(',',""):
            equipment = equipment_info
            continue

    try:
        today_date = time.strftime('%Y-%m-%d')
        cursor.execute(
          f"""
           insert into DB_Schema.operation_data (hospital_name, hospital_address, option_name, price, link_url, info_source, date , shot , region, tier, equipment)
            values('{list[0]}', '{list[1]}', '{list[2].replace(',',"")}', {list[3].replace(",","")}, '{list[4]}', '{list[5]}', '{today_date}' , '{shot_name}', '{region_name}','{tier}','{equipment}')
           """
        )
        connection.commit()
        # print("쿼리가 성공적으로 실행되었습니다")
    except Error as e:
        print(f"다음 오류가 발생했습니다: '{e}'")

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"다음 오류가 발생했습니다: '{e}'")
        return None
    