import time
import datetime
import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def run_real_speedtest():
    file_path = os.path.join(os.path.dirname(__file__), "speed_history.txt")
    
    # Настройки "невидимки"
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        now = datetime.datetime.now().strftime('%H:%M:%S')
        print(f"[{now}] 🌐 Запуск браузерного теста (Яндекс)...")
        
        driver.get("https://yandex.ru")
        time.sleep(5) 

        # Поиск и клик кнопки
        btn = driver.find_element(By.XPATH, "//button[contains(., 'Измерить')]")
        driver.execute_script("arguments[0].click();", btn)
        
        print("⏳ Замер идет (ждем появления цифр)...")
        
        # Динамическое ожидание результата (до 90 сек)
        for _ in range(45): 
            results_text = driver.find_element(By.TAG_NAME, "body").text
            speeds = re.findall(r'(\d+[.,]\d+|\d+)\s*Мбит/с', results_text)
            
            if len(speeds) >= 2: # Нашли и входящую, и исходящую
                dl, ul = speeds[0], speeds[1]
                break
            time.sleep(2)
        else:
            dl, ul = "0", "0"

        # Запись результата
        timestamp = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        log_entry = f"[{timestamp}] Входящая: {dl.replace(',', '.')} Mbps | Исходящая: {ul.replace(',', '.')} Mbps\n"
        
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(log_entry)
        
        print(f"✅ Результат зафиксирован: {dl} / {ul} Mbps")

    except Exception as e:
        print(f"❌ Ошибка: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    # Запуск раз в 30 минут (бесконечный цикл)
    while True:
        run_real_speedtest()
        print("💤 Сплю 30 минут до следующего замера...")
        time.sleep(1800) 
