import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
# НЕ используем headless, чтобы ты видел процесс
chrome_options.add_argument("--start-maximized")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    print("Открываю Яндекс.Интернетометр...")
    driver.get("https://yandex.ru/internet/")
    
    # 1. Ждем и закрываем мешающие окна (если есть)
    time.sleep(5)
    
    # 2. Пытаемся найти кнопку всеми способами
    print("Ищу кнопку 'Измерить'...")
    wait = WebDriverWait(driver, 15)
    
    # Список возможных селекторов кнопки (Яндекс их меняет)
    selectors = [
        "//button[contains(@class, 'button') and contains(., 'Измерить')]",
        "//button[contains(., 'Измерить')]",
        ".p-speed-test__button",
        "button[type='button']"
    ]
    
    btn = None
    for selector in selectors:
        try:
            by = By.XPATH if selector.startswith("/") else By.CSS_SELECTOR
            btn = driver.find_element(by, selector)
            if btn.is_displayed():
                print(f"Нашел кнопку через: {selector}")
                break
        except:
            continue

    if btn:
        # Нажимаем через JS, чтобы игнорировать перекрытия
        driver.execute_script("arguments[0].click();", btn)
        print("🚀 Кнопка нажата! Ждем результатов...")
    else:
        print("❌ Кнопка не найдена. Возможно, страница не прогрузилась.")
        driver.save_screenshot("error_page.png") # Сохраним скриншот, чтобы понять что не так

    # 3. Ожидание результата
    # Ищем элемент, где цифры скорости
    result_xpath = "//div[contains(@class, 'result-value')]"
    wait.until(EC.visibility_of_element_located((By.XPATH, result_xpath)))
    
    print("Вижу начало замера... жду финала (40 сек)")
    time.sleep(45) # Полный цикл замера

    # 4. Вывод данных
    # Ищем блоки Download и Upload
    try:
        dl = driver.find_element(By.XPATH, "//*[contains(@class, 'download')]//*[contains(@class, 'value')]").text
        ul = driver.find_element(By.XPATH, "//*[contains(@class, 'upload')]//*[contains(@class, 'value')]").text
        print(f"\n✅ ИТОГ: Входящая: {dl} Мбит/с | Исходящая: {ul} Мбит/с")
    except:
        # Если классы не совпали, выведем все найденные цифры
        vals = driver.find_elements(By.XPATH, result_xpath)
        res = [v.text for v in vals if v.text]
        print(f"\n✅ ИТОГ: {res}")

except Exception as e:
    print(f"\n Ошибка выполнения: {e}")

finally:
    print("\nЗакрытие через 10 секунд...")
    time.sleep(10)
    driver.quit()
