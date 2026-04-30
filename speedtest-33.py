import time
import datetime
import os
import re
import winsound  # Для звука "БИП"
from plyer import notification  # Для уведомления на рабочем столе
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# 1. Настройка
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

file_path = os.path.join(os.path.dirname(__file__), "speed_history.txt")

try:
    print("Открываю Яндекс.Интернетометр...")
    driver.get("https://yandex.ru/internet/")
    time.sleep(5)

    print("Нажимаю 'Измерить'...")
    btn = driver.find_element(By.XPATH, "//button[contains(., 'Измерить')]")
    driver.execute_script("arguments[0].click();", btn)
    
    print("Замер пошел! Ждем 65 секунд...")
    time.sleep(65)

    # 2. Сбор данных
    try:
        results_text = driver.find_element(By.TAG_NAME, "body").text
        print("Данные получены, обрабатываю...")
    except:
        results_text = "Не удалось прочитать текст страницы"

    # 3. Обработка результатов
    timestamp = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    speeds = re.findall(r'(\d+[.,]\d+|\d+)\s*Мбит/с', results_text)
    
    dl = speeds[0] if len(speeds) > 0 else "0"
    ul = speeds[1] if len(speeds) > 1 else "0"

    # Превращаем входящую скорость в число для проверки (заменяем запятую на точку)
    try:
        val_dl = float(dl.replace(',', '.'))
    except:
        val_dl = 0

    # 4. УВЕДОМЛЕНИЕ НА РАБОЧИЙ СТОЛ
    msg = f"Входящая: {dl} Мбит/с\nИсходящая: {ul} Мбит/с"
    notification.notify(
        title='Результат замера скорости',
        message=msg,
        app_name='SpeedTest',
        timeout=10  # Время показа в секундах
    )

    # 5. ЗВУКОВОЙ СИГНАЛ (БИП), если скорость ниже 30 Мбит/с
    if 0 < val_dl < 30:
        print(f"⚠️ ВНИМАНИЕ: Низкая скорость ({dl} Мбит/с)! Пищу...")
        winsound.Beep(1000, 1000) # Частота 1000Гц, длительность 1 сек

    # 6. ЗАПИСЬ В ФАЙЛ
    with open(file_path, "a", encoding="utf-8") as f:
        log_entry = f"[{timestamp}] Входящая: {dl} Мбит/с | Исходящая: {ul} Мбит/с\n"
        f.write(log_entry)
    
    print(f"✅ Результаты зафиксированы: {dl} / {ul}")

except Exception as e:
    print(f"❌ Произошла ошибка: {e}")
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"Ошибка при запуске: {e}\n")

finally:
    driver.quit()
