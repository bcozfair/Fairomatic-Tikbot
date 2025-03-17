from fuzzywuzzy import process
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from fuzzywuzzy import fuzz
import time

# เชื่อมต่อ Chrome ที่เปิดอยู่
options = webdriver.ChromeOptions()
options.debugger_address = "127.0.0.1:9222"
driver = webdriver.Chrome(options=options)

driver.get("https://www.tiktok.com/@mheeprintv2/live")  # เปิด TikTok Live (ต้องเปิด Live เองก่อน)
wait = WebDriverWait(driver, 10)  # รอสูงสุด 10 วินาที

# หาช่องแชทที่มี class 'css-1l5p0r-DivEditor e1ciaho81'
try:
    chat_box = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "css-1kvtqrg-DivEditor")))
    print("✅ พบช่องแชท")
except:
    print("❌ ไม่พบช่องแชท! ตรวจสอบ class หรือ XPath อีกครั้ง")
    driver.quit()
    exit()

# ตั้งค่าข้อความตอบกลับอัตโนมัติ
auto_replies = {
    "สวัสดี": "สวัสดีครับ Mheeprint ยินดีต้อนรับ!",
    "สั่งซื้อยังไง": "วิธีสั่งซื้อ 1.กดตระกร้า 2.กดรูปสินค้า 3.กดปุ่มแชท อยู่ด้านล่าง ส่งรูปและข้อความในแชทได้เลยครับ",
    "กดตรงไหน": "วิธีสั่งซื้อ 1.กดตระกร้า 2.กดรูปสินค้า 3.กดปุ่มแชท อยู่ด้านล่าง ส่งรูปและข้อความในแชทได้เลยครับ",
    "ส่งรูปทางไหน": "วิธีสั่งซื้อ 1.กดตระกร้า 2.กดรูปสินค้า 3.กดปุ่มแชท อยู่ด้านล่าง ส่งรูปและข้อความในแชทได้เลยครับ",
    "ทำยังไง": "วิธีสั่งซื้อ 1.กดตระกร้า 2.กดรูปสินค้า 3.กดปุ่มแชท อยู่ด้านล่าง ส่งรูปและข้อความในแชทได้เลยครับ",
    "ได้มั้ย": "ออกแบบเองได้เลยครับ ใส่ชื่อ ใส่รูป ใส่ข้อความ แจ้งแอดมินทางแชทได้เลยนะครับ",
    "ซื้อ": "วิธีสั่งซื้อ 1.กดตระกร้า 2.กดรูปสินค้า 3.กดปุ่มแชท อยู่ด้านล่าง ส่งรูปและข้อความในแชทได้เลยครับ",
    "ยังไง": "วิธีสั่งซื้อ 1.กดตระกร้า 2.กดรูปสินค้า 3.กดปุ่มแชท อยู่ด้านล่าง ส่งรูปและข้อความในแชทได้เลยครับ",
    "รูป": "วิธีสั่งซื้อ 1.กดตระกร้า 2.กดรูปสินค้า 3.กดปุ่มแชท อยู่ด้านล่าง ส่งรูปและข้อความในแชทได้เลยครับ",
    "ออกแบบ": "ส่งรูปและข้อความในแชท ให้เราออกแบบให้ได้เลยครับ",
    "ราคา": "ลูกค้า กดดูราคา ในตระกร้านะครับ ราคารวมค่าออกแบบแล้วครับ ไม่มี+เพิ่มนะครับ",
    "เท่าไร": "ลูกค้า กดดูราคา ในตระกร้านะครับ ราคารวมค่าออกแบบแล้วครับ ไม่มี+เพิ่มนะครับ",
    "กี่บาท": "ลูกค้า กดดูราคา ในตระกร้านะครับ ราคารวมค่าออกแบบแล้วครับ ไม่มี+เพิ่มนะครับ",
    "ซื้อแล้ว": "Mheeprint ขอบพระคุณที่อุดหนุนครับ",
    "สั่งแล้ว": "Mheeprint ขอบพระคุณที่อุดหนุนครับ",
    "ขอดู": "แจ้งเลขออเดอร์ 4 ตัวท้าย ดูการยิงเลเซอร์ได้เลยครับ หากไม่ทราบให้ทักแชทหาแอดมินนะครับ",
    "ดู": "แจ้งเลขออเดอร์ 4 ตัวท้าย ดูการยิงเลเซอร์ได้เลยครับ หากไม่ทราบให้ทักแชทหาแอดมินนะครับ",
    "วันไหน": "ลูกค้าสั่งวันนี้ ร้านผลิตส่งด่วนพรุ่งนี้ทันที จะได้รับรูปที่ออกแบบพรุ่งนี้ทางแชท ก่อน 11 โมงครับ รบกวน ยืนยันแบบหรือแจ้งแก้ไข ก่อนเที่ยง หากร้านเริ่มผลิตแล้วไม่สามารถแก้ไขได้นะครับ",
    "วันนี้": "ลูกค้าสั่งวันนี้ ร้านผลิตส่งด่วนพรุ่งนี้ทันที จะได้รับรูปที่ออกแบบพรุ่งนี้ทางแชท ก่อน 11 โมงครับ รบกวน ยืนยันแบบหรือแจ้งแก้ไข ก่อนเที่ยง หากร้านเริ่มผลิตแล้วไม่สามารถแก้ไขได้นะครับ",
    "นานไหม": "สั่งวันนี้ ร้านผลิตส่งด่วนพรุ่งนี้ทันที ขนส่งเดินทาง 2-3วัน ได้รับของครับ",
    "ส่ง": "สั่งวันนี้ ร้านผลิตส่งด่วนพรุ่งนี้ทันที ขนส่งเดินทาง 2-3วัน ได้รับของครับ"
}

# ฟังก์ชันส่งข้อความโดยใช้ Selenium
def send_message(text):
    chat_input = driver.find_element(By.CLASS_NAME, "css-1kvtqrg-DivEditor")
    chat_input.clear()  # ล้างข้อความเก่าในช่อง
    chat_input.send_keys(text)  # พิมพ์ข้อความ
    chat_input.send_keys(Keys.ENTER)  # กด Enter เพื่อส่งข้อความ
    print(f"✅ ส่งข้อความ: {text}")

# ฟังก์ชันตอบกลับข้อความที่คล้าย
def get_best_reply(text):
    for key in auto_replies:
        similarity = fuzz.partial_ratio(key, text)
        if similarity > 80:  # ถ้าความคล้ายกันมากกว่า 80%
            return auto_replies[key]
    return None

# ตัวแปรเก็บข้อความที่ได้ตอบไปแล้ว
answered_messages = set()

# วนลูปตรวจสอบข้อความใหม่ และตอบกลับ
while True:
    try:
        # รอให้ข้อความแชทโหลด
        wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'DivComment')]")))

        # ดึงข้อความแชท
        chat_messages = driver.find_elements(By.XPATH, "//div[contains(@class, 'DivComment')]")

        # แสดงข้อความทั้งหมด
        for msg in chat_messages:
            text = msg.text.strip()
            print(f"💬 ข้อความจาก Live: {text}")

            # หลีกเลี่ยงการตอบกลับข้อความซ้ำ
            if text in answered_messages:
                continue

            # ค้นหาคำตอบที่ใกล้เคียง
            reply = get_best_reply(text)
            if reply:
                send_message(reply)  # ส่งข้อความ
                print(f"✅ ตอบกลับ: {reply}")
                answered_messages.add(text)  # เก็บข้อความที่ตอบไปแล้ว
                time.sleep(150)  # รอ 2 วินาที ป้องกันส่งถี่เกินไป

        time.sleep(5)  # รอให้หน้าเว็บโหลดก่อน

    except Exception as e:
        print("❌ เกิดข้อผิดพลาด:", e)
        break

driver.quit()
