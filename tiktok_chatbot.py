from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# 1️⃣ ตั้งค่าให้ Selenium เชื่อมต่อกับ Chrome ที่เปิดอยู่
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9222"  # ใช้พอร์ตที่เปิด Remote Debugging

# 2️⃣ เปิด WebDriver โดยไม่เปิด Chrome ใหม่
driver = webdriver.Chrome(options=options)
driver.get("https://www.tiktok.com/@mheeprintv2/live")  # ไปที่ TikTok Live (ให้เปิด Live เองก่อน)

time.sleep(5)  # รอให้หน้าเว็บโหลด

# 3️⃣ วนลูปดึงข้อความจากแชท TikTok Live
while True:
    try:
        messages = driver.find_elements(By.CLASS_NAME, "chat-message-class")  # แก้ class ให้ตรงกับ TikTok

        for msg in messages:
            print("💬 ข้อความจาก Live:", msg.text)

        time.sleep(3)  # หน่วงเวลาเพื่อไม่ให้โหลดบ่อยเกินไป

    except Exception as e:
        print("❌ เกิดข้อผิดพลาด:", e)
        break

driver.quit()
