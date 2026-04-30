from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pytest

def test_google_open():
    # 1. Инициализация драйвера (как в вашем файле speedtest-3.py)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    try:
        # 2. Действие: открываем сайт
        driver.get("https://www.google.com")
        
        # 3. ПРОВЕРКА: есть ли слово Google в заголовке вкладки?
        assert "Google" in driver.title
        
    finally:
        # 4. Закрытие браузера (ОБЯЗАТЕЛЬНО, чтобы не засорять память)
        driver.quit()
