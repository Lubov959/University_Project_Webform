import unittest
from app import app


class TestFormSubmission(unittest.TestCase):

    def setUp(self):
        # Этот метод запускается ПЕРЕД каждым тестом

        # Создаём тестовый клиент Flask-приложения
        # Он имитирует браузер, но без реального запуска сервера
        self.client = app.test_client()

        # Включаем тестовый режим Flask
        # Это упрощает обработку ошибок и делает тестирование предсказуемым
        self.client.testing = True



    def test_empty_fields_returns_400(self):
        # Отправляем POST-запрос на маршрут /submit
        # Все поля формы передаются как пустые строки
        response = self.client.post('/submit', data={
            'name': '',
            'day': '',
            'language': '',
            'color': ''
        })

        # Проверяем HTTP-статус ответа
        # Ожидаем 400 (Bad Request), потому что форма невалидна
        self.assertEqual(response.status_code, 400)

        # Проверяем, что файл НЕ был отправлен пользователю
        # Если бы файл отправлялся, появился бы заголовок Content-Disposition
        self.assertNotIn('Content-Disposition', response.headers)


    def test_partially_filled_fields_returns_400(self):
        # Отправляем форму, где часть данных отсутствует
        response = self.client.post('/submit', data={
            'name': 'John',      # заполнено
            'day': '',           # пусто
            'language': '',      # пусто
            'color': 'red'       # заполнено
        })

        # Сервер должен отклонить запрос, так как не все поля заполнены
        self.assertEqual(response.status_code, 400)

        # Файл не должен быть сформирован и отправлен
        self.assertNotIn('Content-Disposition', response.headers)


    def test_invalid_name_with_numbers(self):
        response = self.client.post('/submit', data={
            'name': 'John123',
            'day': 'Monday',
            'language': 'Python',
            'color': 'blue'
        })

        # backend должен защититься
        self.assertEqual(response.status_code, 400)


    def test_valid_form_returns_file(self):
        # Отправляем полностью заполненную форму
        response = self.client.post('/submit', data={
            'name': 'John',
            'day': 'Monday',
            'language': 'Python',
            'color': 'blue'
        })

        # Ожидаем успешный ответ от сервера
        self.assertEqual(response.status_code, 200)

        # Проверяем, что сервер действительно отправил файл
        self.assertIn('Content-Disposition', response.headers)

        # Достаём заголовок Content-Disposition
        # В нём хранится информация о скачиваемом файле
        content_disposition = response.headers.get('Content-Disposition')

        # Проверяем, что файл отправляется как attachment (скачивание)
        self.assertIn('attachment', content_disposition)

        # Проверяем, что имя файла содержит имя пользователя
        self.assertIn('John', content_disposition)




if __name__ == '__main__':
    # Запускает все тесты в этом файле
    unittest.main()