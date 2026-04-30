import requests

# Регистрационные данные
registration_data = {
    'email': 'test@example.com',           # testpost@mail.ru
    'password': 'SecurePassword123!',     # testpost
    'confirm_password': 'SecurePassword123!'  # testpost
}

def register_test():
    """
    Отправляет POST-запрос на регистрацию нового пользователя
    """
    try:
        # Отсылаем POST-запрос на регистрацию
        response = requests.put('http://2.59.41.2:6700/auth/register', data=registration_data)
        
        # Анализируем полученный ответ
        if response.status_code == 200 or response.status_code == 201:
            print("Регистрация прошла успешно!")
        else:
            print(f"Ошибка регистрации. Статус-кода: {response.status_code}, Ответ сервера: {response.text}")
    
    except Exception as e:
        print(f"Возникла ошибка: {e}")

if __name__ == '__main__':
    register_test()