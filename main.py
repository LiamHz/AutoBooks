from selenium import webdriver
from selenium.webdriver.common.keys import Keys
#Enable waiting
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import ffmpy
import os

from wavenet import text_to_speech

from oauth2client import file


# Type in powershell
# $env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\liamh\Documents\auth\AutoBooks-fa53d14aa157.json"

user_input = input("What Medium article do you want to TTS?")
print("TTSing now")

driver = webdriver.Chrome("chromedriver.exe")

driver.get(user_input)

article_text_xpath = "//div[@class='section-content']"

# Wait until Medium post loads
try:
    elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, article_text_xpath))
    )
except TimeoutException:
    pass

article_text = driver.find_element_by_xpath(article_text_xpath).text
# print(article_text)

text_to_speech(article_text[102:5000])

# Generate video for YouTube upload
def convert_mp3_to_mp4(mp3, img):
    os.system("ffmpeg -loop 1 -i {} -i {} -c:a copy -c:v libx264 -shortest out.mp4".format(img, mp3))

convert_mp3_to_mp4("output.mp3", "manz.png")

# Upload mp4 to YouTube
os.system("youtube-upload --title='TEST' --playlist='AutoBooks' out.mp4")
