import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.add_argument("-profile")
options.add_argument(r"C:\User\AppData\Roaming\Mozilla\Firefox\Profiles\XXXXXXXX.default-release") # change it to your profile path, found typing about:profiles on firefox

driver = webdriver.Firefox(options=options)
driver.get("https://www.youtube.com/playlist?list=WL") # replace by your playlist link

file_path = r"c:\User\exemple\scrapped_links.txt" # change the patch to where you whant your output file to be created

try:
    video_links = set()
    batch = []
    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a#video-title"))
    )
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    while True:
        videos = driver.find_elements(By.CSS_SELECTOR, "a#video-title")
        for video in videos:
            link = video.get_attribute("href")
            if link not in video_links:
                video_links.add(link)
                batch.append(link)
        if len(batch) >= 100:
            with open(file_path, "a", encoding="utf-8") as file:
                for link in batch:
                    file.write(link + "\n")
            batch.clear()
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    if batch:
        with open(file_path, "a", encoding="utf-8") as file:
            for link in batch:
                file.write(link + "\n")
finally:
    driver.quit()
