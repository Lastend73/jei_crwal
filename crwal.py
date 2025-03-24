from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

from fake_useragent import UserAgent

import crwal_setting as crwal
import db_test as db

import time
import csv
import re

from datetime import datetime
import pprint

def gangnamunni_crawl_data(driver, main_window, num):
    
    price_CSS_SELECTOR ='.flex.flex-row.border.border-gray-200.rounded-lg > div > .flex.flex-col >.flex.flex-row.typo-subTitle1Bold.text-typography-primary'
    option_name_CSS_SELECTOR ='.flex.flex-row.border.border-gray-200.rounded-lg > div > h3'
    hospital_name_CSS_SELECTOR ='#hospital-page-text-title-hospitalname'
    hospital_address_CSS_SELECTOR ='.HospitalMap__StyledAddressWrapper-sc-11eb21fc-0.eaGrCG.addressWrapper > address'
    info_list = []
    try:
        more_button = driver.find_element(By.XPATH, f'//*[@id="event-card-component-ui-{num}"]')
        href_value = more_button.get_attribute("href")
        driver.execute_script("window.open('" + href_value + "')")
        print(f"num: {num}, href: {href_value}")
        driver.implicitly_wait(5)

        # 창 현재창인지 확인
        for handle in driver.window_handles:
            if handle != main_window:
                driver.switch_to.window(handle)
                break

        
        # 가격 및 옵션 추출
        try:
            price = driver.find_elements(By.CSS_SELECTOR, price_CSS_SELECTOR)
        except TimeoutException:
            print("가격출력 에러")
        try:
            option_name = driver.find_elements(By.CSS_SELECTOR, option_name_CSS_SELECTOR)
        except TimeoutException:
            print("옵션출력 에러")

        driver.implicitly_wait(5)
        # 병원명, 병원주소, 시술명, 가격, url
        info = []
        url = driver.current_url
        # 버튼 클릭하여 병원 정보 추출
        for a in range(len(price)):
            info.append([option_name[a].text if option_name else "", price[a].text[0:-1] if price else "", url, "강남언니"])

        try:
            hospital_info_button = driver.find_element(By.XPATH, '//*[@id="screenMain"]/div[2]/div[2]/a')
            driver.execute_script("arguments[0].click();", hospital_info_button)
        except NoSuchElementException:
            print("병원 버튼을 찾을 수 없습니다.")
            crwal.nordvpn()

        try : 
            hospital_name = driver.find_element(By.CSS_SELECTOR, hospital_name_CSS_SELECTOR).text
        except :
            print("병원명 찾기불가")
        
        try :
            hospital_address_full = driver.find_element(By.CSS_SELECTOR, hospital_address_CSS_SELECTOR).text
        except :
            print("병원명 찾기 불가")

        for b in info:
            b.insert(0, hospital_name)
            b.insert(1, hospital_address_full)

        
        driver.close()
        # 메인 창으로 전환
        driver.switch_to.window(main_window)
        return info
    except TimeoutException:
        print("스킵")
        # 새 창 닫기
        driver.close()
        # 메인 창으로 전환
        driver.switch_to.window(main_window)
    except NoSuchElementException as e:
        print(f"요소를 찾을 수 없습니다: {e}")
        # 새 창 닫기
        driver.close()
        # 메인 창으로 전환
        driver.switch_to.window(main_window)
    except Exception as e:
        print("2222")
        print(f"예외 발생: {e}")
        # 새 창 닫기
        driver.close()
        # 메인 창으로 전환
        driver.switch_to.window(main_window)
    if info_list == []:
        print("")
    else:
        return info_list

def gangnamunni_crawl():
    info_list = []
    try:
        driver = crwal.crwal_setting(f'https://www.gangnamunni.com/events?q=%EB%A6%AC%ED%94%84%ED%8C%85')

        scroll_location = driver.execute_script("return document.body.scrollHeight")
        try:
            event_count = int(driver.find_element(By.CSS_SELECTOR, '.irAqsc').text.replace(",", ""))
        except NoSuchElementException:
            event_count = 0
        print(event_count)
        if event_count > 20:
            try:
                more_button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.kTmIRB ')))
                driver.execute_script("arguments[0].click();", more_button)
                print("A")
            except NoSuchElementException:
                print("더보기 버튼을 찾을 수 없습니다.")

        driver = crwal.scroll(driver, scroll_location)

        main_window = driver.current_window_handle
        count_num = 0
        refuse_num = 0

        for i in range(event_count):
            a = gangnamunni_crawl_data(driver, main_window, i)
            if a is not None:
                info_list.extend(a)
                for data in a :
                    # print(a)
                    db.execute_query(data)
            

            count_num += 1
            refuse_num += 1

            print(f"{count_num} / {event_count}")
            if refuse_num > 50:
                crwal.nordvpn()
                refuse_num = 0
        driver.quit()
    except Exception as e:
        print(f"예외 발생: {e}")
        print("여기입니다다")
        driver.quit()
    return info_list
