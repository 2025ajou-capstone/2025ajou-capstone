from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

login_url = "https://www.safetyreport.go.kr/#/main/login/login"
traffic_report_url = "https://www.safetyreport.go.kr/#safereport/safereport3"
upload_file_path = "C:\\blackbox_file\\250418.jpg"

violation_type = "Test type"
location = "판교역로 2"
plate_number = "123가5678"
violation_date = "1999.06.03"
violation_hour = "5"
violation_minute = "6"
phone_number = "Test mobile"

user_id = "kakaokokoa"
user_pw = "wotjr7134!"

# 텍스트형 먼저 입력 -> 위치 등록 -> 파일 입력 -> 신고 OR 임시저장 FLOW
def report_traffic(violation_type, location, plate_number, violation_date, violation_hour,violation_minute, phone_number):
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    # EC2에선 headless 모드 사용 가능
    # chrome_options.add_argument("--headless")

    service = Service()  # 자동으로 크롬 드라이버 경로 잡아줌 (pip install chromedriver-autoinstaller 권장)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    report_title = "Make title"
    report_contents = "Descript report"

    try:
        driver.get(login_url)

        time.sleep(3)
    
        # login
        driver.find_element(By.ID, "username").send_keys(user_id)
        driver.find_element(By.ID, "password").send_keys(user_pw)
        login_button = driver.find_element(By.CSS_SELECTOR, ".button.big.blue")
        login_button.click()
        time.sleep(1)

        driver.get(traffic_report_url)
        time.sleep(2)      # 대신 WebDriverWait 사용 고려, 성능 최적화를 위해서

        # 키보드 보안 프로그램 설치 팝업 -> 취소
        try:
            alert = driver.switch_to.alert
            print("팝업 메시지:", alert.text)
            alert.dismiss()  # "취소" 버튼 클릭
            print("✅ 보안 설치 팝업 무시")
        except NoAlertPresentException:
            print("팝업 없음, 계속 진행")


        # 위반 유형 선택 드롭다운
        select_element = driver.find_element(By.ID, "ReportTypeSelect")
        # Selenium Select 객체로 감싸기
        select = Select(select_element)

        # value 값으로 선택 (예: "02" = 교통위반)  -> 자세한 value는 아래 참고
        select.select_by_value("02")
        time.sleep(1)  

        driver.find_element(By.ID, "C_A_TITLE").send_keys(report_title)
        driver.find_element(By.ID, "C_A_CONTENTS").send_keys(report_contents)
        time.sleep(1)  

        driver.find_element(By.ID, "VHRNO").send_keys(plate_number)

        date_input = driver.find_element(By.ID, "DEVEL_DATE")
    
        # 1. 기존 날짜 지우기
        date_input.clear()
        date_input.send_keys(violation_date)
        date_input.send_keys(Keys.ENTER)
        
        select_hour = Select(driver.find_element(By.ID, "DEVEL_TIME_HH"))
        select_hour.select_by_value(violation_hour.zfill(2))  # 예: "7" → "07"

        select_min = Select(driver.find_element(By.ID, "DEVEL_TIME_MM"))
        select_min.select_by_value(violation_minute.zfill(2))  # 예: "5" → "05"

        # 도로명 주소 입력
        main_window = driver.current_window_handle
        driver.find_element(By.ID, "btnFindLoc").click()
       
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1) # 새 창이 열릴 때까지 대기

        for handle in driver.window_handles:     # 새 창으로 포커스 전환
            if handle != main_window:
                driver.switch_to.window(handle)
                break
    
        iframe = driver.find_element(By.XPATH, '//iframe[@title="우편번호 검색 프레임"]') #iframe 이동
        driver.switch_to.frame(iframe)
        #print("현재 창 제목:", driver.title)
        driver.find_element(By.ID, "region_name").send_keys(location)
        driver.find_element(By.XPATH, '//*[@id="searchForm"]/fieldset/div/button[2]').click()
        driver.find_element(By.XPATH, '//*[@id="focusContent"]/ul/li[1]/dl/dd[1]/span/button').click()
        driver.switch_to.window(main_window)
        #print("현재 창 제목:", driver.title)

        # 파일 등록 기능능
        iframe = driver.find_element(By.XPATH, '//*[@id="raonkuploader_frame_kupload1"]') #iframe 이동
        driver.switch_to.frame(iframe)
        # driver.find_element(By.ID,"button_add").click() -> 업로드 파일 버튼

        container = driver.find_element(By.ID, "RAON_K_UP_wrapper") # 파일 업로드 input 요소 찾기
        file_input = container.find_element(By.CSS_SELECTOR, 'input[type="file"]')
        file_input.send_keys(upload_file_path)
        driver.switch_to.window(main_window)
        
        # 임시 저장 XPATH
        driver.find_element(By.XPATH, '//*[@id="frmSafeReport"]/div[2]/article/div/div[6]/a[2]').click()
        # 신고 XPATH: //*[@id="frmSafeReport"]/div[2]/article/div/div[6]/a[3]
        time.sleep(1000)  


#//*[@id="searchForm"]/fieldset/div/button[2]
    except Exception as e:
        print(f"🚨 Error {e}")

    finally:
        driver.quit()


report_traffic(violation_type, location, plate_number, violation_date, violation_hour,violation_minute, phone_number)



# <option value="">유형을 선택해주세요.
# </option><option value="02">교통위반(고속도로 포함)
# </option><option value="03">이륜차 위반
# </option><option value="05">버스전용차로 위반(고속도로제외)
# </option><option value="06">번호판 규정 위반
# </option><option value="07">불법등화, 반사판(지) 가림·손상
# </option><option value="08">불법 튜닝, 해체, 조작
# </option><option value="09">기타 자동차 안전기준 위반</option></select>