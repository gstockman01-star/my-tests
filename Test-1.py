import requests

# Данные для отправки
data = {
    'username': 'test_user',   # primer@mail.ru
    'password': 'test_password'  # primer1@mail.ru
}

def test_login():
    try:
        response = requests.post('http://2.59.41.2:6700/auth/login', data=data)
        
        if response.status_code == 200:
            print("Авторизация прошла успешно.")
        else:
            print(f"Ошибка авторизации. Код статуса: {response.status_code}")
            
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    test_login()