import requests

# Данные для отправки
data = {
    'username': 'your_username_here',   # prime@mail.ru
    'password': 'your_password_here'    # prime1@mail.ru
}

def test_login():
    try:
        response = requests.post('http://2.59.41.2:6700/auth/login', data=data)
    
        if response.status_code == 200:
            print("Авторизация прошла успешно.")
        elif response.status_code in (401, 403):
            print("Ошибка авторизации. Возможно неверные учётные данные.")
        else:
            print(f"Ошибка авторизации. Код статуса: {response.status_code}. Ответ сервера: {response.text}")
                
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    test_login()