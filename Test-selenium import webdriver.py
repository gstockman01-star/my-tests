from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# 1. Настройка драйвера (скачается автоматически, если его нет)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    # 2. Переход на сайт
    driver.get("https://www.google.com")
    
    # 3. Проверка заголовка страницы
    print(f"Заголовок открытой страницы: {driver.title}")
    
    if "Google" in driver.title:
        print("Успех! Selenium работает корректно.")
    else:
        print("Что-то пошло не так: заголовок не совпадает.")

finally:
    # 4. Закрытие браузера
    driver.quit()
