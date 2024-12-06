
# HelpDB

HelpDB - это простая в использовании библиотека для работы с SQLite базами данных в Python. Она предоставляет удобный интерфейс для выполнения основных операций с базой данных.

## Установка

```
pip install helpdb
```

## Основное использование

```python
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
```

## Основные методы

- `create_table(table_name, columns)` - создание новой таблицы
- `insert(table_name, data)` - вставка данных в таблицу
- `select(table_name, columns=None, where=None, params=())` - выборка данных из таблицы
- `update(table_name, data, where, params=())` - обновление данных в таблице
- `delete(table_name, where, params=())` - удаление данных из таблицы
- `execute_safe(query, params=())` - безопасное выполнение SQL-запроса с поиском похожих таблиц при ошибках

## Дополнительные возможности

- Автоматический поиск похожих таблиц при опечатках
- Экспорт и импорт данных в формате JSON
- Создание резервных копий базы данных

## Документация

Для просмотра полной документации выполните команду:

```
python -m helpdb
```

Это откроет веб-страницу с подробной документацией и примерами использования библиотеки.
