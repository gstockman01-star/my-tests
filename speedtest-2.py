import time
import datetime
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# 1. Настройка
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Путь к файлу в той же папке, где этот скрипт
file_path = os.path.join(os.path.dirname(__file__), "speed_history.txt")

try:
    print("Открываю Яндекс.Интернетометр...")
    driver.get("https://yandex.ru/internet/")
    time.sleep(5)

    print("Нажимаю 'Измерить'...")
    # Ищем кнопку по тексту "Измерить"
    btn = driver.find_element(By.XPATH, "//button[contains(., 'Измерить')]")
    driver.execute_script("arguments[0].click();", btn)
    
    print("Замер пошел! Ждем 65 секунд...")
    time.sleep(65) # Ждем с запасом, чтобы заполнились оба поля

    # 2. Собираем данные (просто берем весь текст из блока теста)
    try:
        results_text = driver.find_element(By.TAG_NAME, "body").text
        # Ищем строки со скоростью в общем тексте (грубый, но надежный поиск)
        # Мы просто запишем всё, что нашли, в лог для анализа
        print("Данные получены, записываю в файл...")
    except:
        results_text = "Не удалось прочитать текст страницы"

    # 3. ЗАПИСЬ В ФАЙЛ
    timestamp = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"--- Замер от {timestamp} ---\n")
        f.write(results_text[:1000]) # Пишем первые 1000 символов страницы
        f.write("\n\n")
    
    print(f"✅ Готово! Проверь файл: {file_path}")

except Exception as e:
    print(f"❌ Произошла ошибка: {e}")
    # Если ошибка, всё равно создадим файл с текстом ошибки
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"Ошибка при запуске: {e}\n")

finally:
    driver.quit()
