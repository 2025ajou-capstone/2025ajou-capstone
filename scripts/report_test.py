from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoAlertPresentException
from urllib.parse import unquote
import time
import re
import requests

login_url = "https://www.safetyreport.go.kr/#/main/login/login"
traffic_report_url = "https://www.safetyreport.go.kr/#safereport/safereport3"

user_id = "kakaokokoa"
user_pw = "wotjr7134!"

video_path = "D:/Ajou_ISE/Senior_1st/2025ajou-capstone/scripts/video/clip.mp4"  # 업로드할 파일 경로


def extract_raonk(driver):
    time.sleep(1000)  # 로딩 시간 확보
    iframe = driver.find_element(By.ID, "raonkuploader_frame_kupload1")
    src = iframe.get_attribute("src")
    print("iframe src:", src)  # ✅ 확인용
    if "raonk=" in src:
        return src.split("raonk=")[-1]
    return None


def extract_cookie_string(driver):
    cookies = driver.get_cookies()
    return "; ".join([f"{c['name']}={c['value']}" for c in cookies])


def extract_bearer_token(driver):
    cookies = driver.get_cookies()
    for cookie in cookies:
        if cookie['name'] == 'safepeople.auth':
            return unquote(cookie['value'])
    return None


def upload_video_to_raon(upload_url, cookie_str, file_path):
    headers = {
        "Cookie": cookie_str
    }
    files = {
        'uploadfile': (file_path.split("/")[-1], open(file_path, 'rb'), 'video/mp4')
    }
    response = requests.post(upload_url, headers=headers, files=files)
    print("[업로드 응답]:", response.text[:300])  # 일부만 출력

    match = re.search(r'callbackUploadResult\(\"(.+?\.mp4)\"', response.text)
    if match:
        return match.group(1)
    return None


def login_and_prepare_upload():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(login_url)
        time.sleep(2)

        driver.find_element(By.ID, "username").send_keys(user_id)
        driver.find_element(By.ID, "password").send_keys(user_pw)
        driver.find_element(By.CSS_SELECTOR, ".button.big.blue").click()
        time.sleep(3)

        driver.get(traffic_report_url)
        time.sleep(3)

        try:
            alert = driver.switch_to.alert
            print("팝업 메시지:", alert.text)
            alert.dismiss()
        except NoAlertPresentException:
            print("팝업 없음")

        raonk = extract_raonk(driver)
        cookies = extract_cookie_string(driver)
        token = extract_bearer_token(driver)

        print("raonk:", raonk)
        print("token:", token[:40] + "...")

        upload_url = f"https://www.safetyreport.go.kr/raonkupload/handler/raonkhandler.jsp?raonk={raonk}"
        uploaded_filename = upload_video_to_raon(upload_url, cookies, video_path)

        print("업로드된 파일명:", uploaded_filename)

    finally:
        driver.quit()


login_and_prepare_upload()