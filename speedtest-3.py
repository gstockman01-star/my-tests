import time
import datetime
import os
import re
import winsound
from plyer import notification
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# 1. Настройка путей и параметров
file_path = os.path.join(os.path.dirname(__file__), "speed_history.txt")
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    # ВАЖНО: правильный URL
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Запуск фонового замера...")
    driver.get("https://yandex.ru/internet/")
    time.sleep(10) 

    print("Ищу кнопку 'Измерить'...")
    try:
        btn = driver.find_element(By.XPATH, "//button[contains(., 'Измерить')]")
    except:
        btn = driver.find_element(By.CLASS_NAME, "p-speed-test__button")

    # Клик через JS - самый надежный для Headless
    driver.execute_script("arguments[0].click();", btn)
    print("Кнопка нажата! Замер идет (65 сек)...")
    time.sleep(65)
    
    # 2. Сбор данных
    results_text = driver.find_element(By.TAG_NAME, "body").text
    speeds = re.findall(r'(\d+[.,]\d+|\d+)\s*Мбит/с', results_text)
    
    dl = speeds[0] if len(speeds) > 0 else "0"
    ul = speeds[1] if len(speeds) > 1 else "0"

    try:
        val_dl = float(dl.replace(',', '.'))
    except:
        val_dl = 0

    # 3. Уведомление на рабочий стол
    notification.notify(
        title='Замер скорости завершен',
        message=f"Входящая: {dl} Мбит/с\nИсходящая: {ul} Мбит/с",
        app_name='SpeedTest',
        timeout=10
    )

    # 4. Бип при низкой скорости
    if 0 < val_dl < 30:
        print(f"⚠️ Низкая скорость ({dl} Мбит/с)! Бип...")
        winsound.Beep(1000, 1000)

    # 5. Запись в файл
    timestamp = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] Входящая: {dl} Мбит/с | Исходящая: {ul} Мбит/с\n")
    
    print(f"✅ Готово! Результат: {dl} / {ul}")

except Exception as e:
    print(f"❌ Ошибка: {e}")
    driver.save_screenshot("headless_error.png")
    print("Снимок экрана сохранен в headless_error.png")

finally:
    driver.quit()
