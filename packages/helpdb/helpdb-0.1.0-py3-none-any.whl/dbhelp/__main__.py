
import webbrowser
import os
import http.server
import socketserver
import threading

HTML_CONTENT = '''
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HelpDB Documentation</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1, h2 {
            color: #2c3e50;
        }
        code {
            background-color: #f4f4f4;
            padding: 2px 5px;
            border-radius: 3px;
        }
        pre {
            background-color: #f4f4f4;
            padding: 10px;
            border-radius: 5px;
            overflow-x: auto;
        }
    </style>
</head>
<body>
    <h1>HelpDB Documentation</h1>
    
    <h2>Введение</h2>
    <p>HelpDB - это простая в использовании библиотека для работы с SQLite базами данных в Python. Она предоставляет удобный интерфейс для выполнения основных операций с базой данных.</p>
    
    <h2>Установка</h2>
    <pre><code>pip install helpdb</code></pre>
    
    <h2>Основное использование</h2>
    <pre><code>
from helpdb import HelpDB

# Создание экземпляра HelpDB
with HelpDB("example.db") as db:
    # Создание таблицы
    db.create_table("users", {"id": "INTEGER PRIMARY KEY", "name": "TEXT", "age": "INTEGER"})
    
    # Вставка данных
    db.insert("users", {"name": "Алиса", "age": 30})
    db.insert("users", {"name": "Борис", "age": 25})
    
    # Выборка данных
    results = db.select("users", where="age > ?", params=(27,))
    for row in results:
        print(row)
    </code></pre>
    
    <h2>Основные методы</h2>
    <ul>
        <li><code>create_table(table_name, columns)</code> - создание новой таблицы</li>
        <li><code>insert(table_name, data)</code> - вставка данных в таблицу</li>
        <li><code>select(table_name, columns=None, where=None, params=())</code> - выборка данных из таблицы</li>
        <li><code>update(table_name, data, where, params=())</code> - обновление данных в таблице</li>
        <li><code>delete(table_name, where, params=())</code> - удаление данных из таблицы</li>
        <li><code>execute_safe(query, params=())</code> - безопасное выполнение SQL-запроса с поиском похожих таблиц при ошибках</li>
    </ul>
    
    <h2>Дополнительные возможности</h2>
    <ul>
        <li>Автоматический поиск похожих таблиц при опечатках</li>
        <li>Экспорт и импорт данных в формате JSON</li>
        <li>Создание резервных копий базы данных</li>
    </ul>
    
    <h2>Пример использования дополнительных возможностей</h2>
    <pre><code>
# Экспорт таблицы в JSON
db.table_to_json("users", "users.json")

# Импорт данных из JSON в новую таблицу
db.json_to_table("users.json", "users_copy")

# Создание резервной копии базы данных
db.backup("backup.db")

# Использование execute_safe для поиска похожих таблиц при опечатках
results = db.execute_safe("SELECT * FROM usrs")  # Опечатка в имени таблицы
    </code></pre>
</body>
</html>
'''

def run_server(port=8000):
    Handler = http.server.SimpleHTTPRequestHandler
    
    class MyHandler(Handler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode())

    with socketserver.TCPServer(("", port), MyHandler) as httpd:
        print(f"Документация доступна по адресу: http://localhost:{port}")
        httpd.serve_forever()

if __name__ == "__main__":
    port = 8000
    server_thread = threading.Thread(target=run_server, args=(port,))
    server_thread.daemon = True
    server_thread.start()

    webbrowser.open(f"http://localhost:{port}")

    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nСервер остановлен.")
