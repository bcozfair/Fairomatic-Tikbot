from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# ตั้งค่า WebDriver (เปิด TikTok Live)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.get("https://www.tiktok.com/@chiisgamer/live")  # เปลี่ยนเป็น TikTok Live ของคุณ

time.sleep(5)
print("✅ เริ่มดึงข้อความจากแชท...")

# คำตอบที่กำหนดไว้ล่วงหน้า (Rule-Based)
responses = {
    "สวัสดี": "สวัสดีครับ! ยินดีต้อนรับ 😊",
    "ส่งของวันไหน": "เราส่งของทุกวันจันทร์-ศุกร์ครับ!",
    "ร้านอยู่ที่ไหน": "ร้านของเราอยู่ที่ [ระบุที่ตั้งร้าน] ครับ",
    "ราคาเท่าไหร่": "สินค้าของเราราคาเริ่มต้นที่ 199 บาทครับ 😊",
    "มีโปรโมชันไหม": "ตอนนี้เรามีโปรโมชันลด 10% เมื่อสั่งครบ 500 บาทครับ!"
}

# ฟังก์ชันตอบกลับแชทตามเงื่อนไขที่กำหนด
def chatbot_reply(message):
    for keyword, reply in responses.items():
        if keyword in message.lower():
            return reply
    return "ขออภัย ฉันไม่เข้าใจคำถามนี้ครับ 😅"

# ฟังก์ชันส่งข้อความกลับไปที่ TikTok Live
def send_chat_message(message):
    try:
        chat_box = driver.find_element(By.CSS_SELECTOR, "input.chat-input-class")  # ใช้ class ที่ถูกต้อง
        chat_box.send_keys(message)
        chat_box.send_keys(Keys.RETURN)
    except Exception as e:
        print("❌ ไม่สามารถส่งข้อความได้:", e)

# วนลูปดึงข้อความจากแชท TikTok
while True:
    try:
        chat_elements = driver.find_elements(By.CSS_SELECTOR, ".chat-message-class")  # ใช้ class จริง
        for chat in chat_elements:
            message = chat.text
            print("💬 ข้อความจาก Live Chat:", message)

            # ใช้ Rule-Based ตอบกลับ
            reply = chatbot_reply(message)
            print("🤖 Bot ตอบ:", reply)

            # ส่งข้อความกลับไปที่ Live
            send_chat_message(reply)

        time.sleep(2)

    except Exception as e:
        print("❌ เกิดข้อผิดพลาด:", e)
        break


# ใช้ Regular Expression (regex) เพื่อตรวจจับคำที่ใกล้เคียง

import re

def chatbot_reply(message):
    for keyword, reply in responses.items():
        if re.search(rf"\b{keyword}\b", message, re.IGNORECASE):
            return reply
    return "ขออภัย ฉันไม่เข้าใจคำถามนี้ครับ 😅"
