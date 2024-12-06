
import sqlite3
from typing import Any, List, Dict, Union, Optional
import json
import difflib

class HelpDB:
    def __init__(self, db_name: str):
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self):
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()

    def close(self):
        if self.conn:
            self.conn.close()

    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        if not self.conn:
            self.connect()
        return self.cursor.execute(query, params)

    def executemany(self, query: str, params: List[tuple]) -> sqlite3.Cursor:
        if not self.conn:
            self.connect()
        return self.cursor.executemany(query, params)

    def commit(self):
        if self.conn:
            self.conn.commit()

    def rollback(self):
        if self.conn:
            self.conn.rollback()

    def fetchone(self) -> Optional[tuple]:
        return self.cursor.fetchone()

    def fetchall(self) -> List[tuple]:
        return self.cursor.fetchall()

    def create_table(self, table_name: str, columns: Dict[str, str]):
        columns_str = ', '.join([f"{col} {dtype}" for col, dtype in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})"
        self.execute(query)
        self.commit()
        print(f"Таблица '{table_name}' успешно создана.")

    def insert(self, table_name: str, data: Dict[str, Any]):
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.execute(query, tuple(data.values()))
        self.commit()
        print(f"Данные успешно добавлены в таблицу '{table_name}'.")

    def select(self, table_name: str, columns: List[str] = None, where: str = None, params: tuple = ()):
        columns_str = '*' if columns is None else ', '.join(columns)
        query = f"SELECT {columns_str} FROM {table_name}"
        if where:
            query += f" WHERE {where}"
        return self.execute(query, params)

    def update(self, table_name: str, data: Dict[str, Any], where: str, params: tuple = ()):
        set_values = ', '.join([f"{col} = ?" for col in data.keys()])
        query = f"UPDATE {table_name} SET {set_values} WHERE {where}"
        self.execute(query, tuple(data.values()) + params)
        self.commit()
        print(f"Данные в таблице '{table_name}' успешно обновлены.")

    def delete(self, table_name: str, where: str, params: tuple = ()):
        query = f"DELETE FROM {table_name} WHERE {where}"
        self.execute(query, params)
        self.commit()
        print(f"Данные из таблицы '{table_name}' успешно удалены.")

    def table_exists(self, table_name: str) -> bool:
        query = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        result = self.execute(query, (table_name,)).fetchone()
        return result is not None

    def get_table_info(self, table_name: str) -> List[Dict[str, Any]]:
        query = f"PRAGMA table_info({table_name})"
        return [dict(zip(['cid', 'name', 'type', 'notnull', 'dflt_value', 'pk'], row)) for row in self.execute(query)]

    def backup(self, backup_file: str):
        with sqlite3.connect(backup_file) as backup_conn:
            self.conn.backup(backup_conn)
        print(f"Резервная копия базы данных создана в файле '{backup_file}'.")

    def execute_script(self, script: str):
        if not self.conn:
            self.connect()
        self.conn.executescript(script)
        self.commit()
        print("Скрипт SQL успешно выполнен.")

    def query_to_dict(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        cursor = self.execute(query, params)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def table_to_json(self, table_name: str, file_path: str):
        query = f"SELECT * FROM {table_name}"
        data = self.query_to_dict(query)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Таблица '{table_name}' экспортирована в JSON файл '{file_path}'.")

    def json_to_table(self, file_path: str, table_name: str):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if data:
            columns = {key: self._infer_sqlite_type(value) for key, value in data[0].items()}
            self.create_table(table_name, columns)
            for row in data:
                self.insert(table_name, row)
        print(f"Данные из JSON файла '{file_path}' импортированы в таблицу '{table_name}'.")

    @staticmethod
    def _infer_sqlite_type(value: Any) -> str:
        if isinstance(value, int):
            return "INTEGER"
        elif isinstance(value, float):
            return "REAL"
        elif isinstance(value, bool):
            return "BOOLEAN"
        elif isinstance(value, (str, dict, list)):
            return "TEXT"
        else:
            return "BLOB"

    def find_similar_table(self, table_name: str) -> Optional[str]:
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        table_names = [row[0] for row in self.execute(query)]
        matches = difflib.get_close_matches(table_name, table_names, n=1, cutoff=0.6)
        return matches[0] if matches else None

    def execute_safe(self, query: str, params: tuple = ()):
        try:
            return self.execute(query, params)
        except sqlite3.OperationalError as e:
            if "no such table" in str(e):
                table_name = str(e).split(":")[1].strip()
                similar_table = self.find_similar_table(table_name)
                if similar_table:
                    print(f"Таблица '{table_name}' не найдена. Возможно, вы имели в виду '{similar_table}'?")
                    user_input = input("Хотите использовать эту таблицу? (да/нет): ")
                    if user_input.lower() == 'да':
                        new_query = query.replace(table_name, similar_table)
                        return self.execute(new_query, params)
                    else:
                        print("Операция отменена.")
                else:
                    print(f"Таблица '{table_name}' не найдена, и похожих таблиц не обнаружено.")
            else:
                print(f"Произошла ошибка: {e}")
            return None

# Пример использования:
if __name__ == "__main__":
    with HelpDB("example.db") as db:
        db.create_table("users", {"id": "INTEGER PRIMARY KEY", "name": "TEXT", "age": "INTEGER"})
        db.insert("users", {"name": "Алиса", "age": 30})
        db.insert("users", {"name": "Борис", "age": 25})
        results = db.execute_safe("SELECT * FROM usrs")  # Опечатка в имени таблицы
        if results:
            for row in results:
                print(row)
