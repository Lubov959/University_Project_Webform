from flask import Flask, render_template, request, send_file
from docx import Document
import io

# Инициализируем приложение Flask
app = Flask(__name__)


# Главная страница: отображаем HTML-форму
@app.route('/')
def form():
    # Ищет файл form.html в папке templates и отправляет его в браузер
    return render_template('form.html')


# Обработчик данных из формы (срабатывает при нажатии кнопки "Отправить")
@app.route('/submit', methods=['POST'])
def submit():
    # Получаем значения полей из POST-запроса по их атрибуту 'name' в HTML
    name = request.form['name']
    day = request.form['day']
    language = request.form['language']
    color = request.form['color']

    # Создаём новый пустой документ Word в оперативной памяти
    document = Document()

    # Добавляем заголовок (0 — самый крупный стиль)
    document.add_heading('Данные из формы с сайта', 0)

    # Записываем данные в абзацы, используя f-строки для подстановки переменных
    document.add_paragraph(f'Имя: {name}')
    document.add_paragraph(f'Как проходит день: {day}')
    document.add_paragraph(f'Любимый язык: {language}')
    document.add_paragraph(f'Любимый цвет: {color}')

    # Создаём байтовый поток (виртуальный файл в памяти), чтобы не засорять диск реальными файлами
    file_stream = io.BytesIO()
    # Сохраняем созданный документ в этот поток
    document.save(file_stream)
    # Перематываем "курсор" потока в начало, чтобы чтение файла началось с первого байта
    file_stream.seek(0)

    # Отправляем файл обратно в браузер для автоматического скачивания
    return send_file(
        file_stream,
        as_attachment=True,  # Указывает браузеру именно скачать файл, а не открыть его
        download_name=f"{name}.docx",  # Имя файла при сохранении будет равно имени пользователя
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'  # Тип данных для MS Word
    )


# Запуск локального сервера
if __name__ == '__main__':
    # debug=True позволяет серверу автоматически перезагружаться при изменениях в коде
    app.run(debug=True)
