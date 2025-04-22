import json
from datetime import datetime
from typing import List

# Класс для хранения задач
class Task:
    # Счётчик для ID задач, начиная с 1
    counter = 1

    def __init__(self, title, description, category, due_date, priority):
        # Присваиваем задаче уникальный ID и увеличиваем счётчик
        self.id = Task.counter
        Task.counter += 1
        self.title = title  # Название задачи
        self.description = description  # Описание задачи
        self.category = category  # Категория задачи
        self.due_date = due_date  # Срок выполнения
        self.priority = priority  # Приоритет задачи
        self.is_completed = False  # Статус выполнения задачи (по умолчанию - не выполнена)

    # Метод для изменения статуса задачи на "выполнена"
    def mark_complete(self):
        self.is_completed = True

    # Метод для преобразования задачи в словарь (для сохранения в файл)
    def to_dict(self):
        return self.__dict__

    # Статический метод для создания задачи из словаря (для загрузки из файла)
    @staticmethod
    def from_dict(data):
        task = Task(
            data['title'],
            data['description'],
            data['category'],
            data['due_date'],
            data['priority']
        )
        task.id = data['id']
        task.is_completed = data['is_completed']
        return task


# Класс для работы с хранилищем задач
class TaskRepository:
    def __init__(self, filename="tasks.json"):
        self.filename = filename  # Имя файла для хранения задач
        self.tasks: List[Task] = []  # Список задач
        self.load_tasks()  # Загружаем задачи из файла при инициализации

    # Метод для загрузки задач из файла
    def load_tasks(self):
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)  # Читаем задачи из файла
                self.tasks = [Task.from_dict(d) for d in data]  # Преобразуем данные в объекты задач
                # Обновляем счётчик ID, если задачи уже есть
                if self.tasks:
                    Task.counter = max(t.id for t in self.tasks) + 1
        except (FileNotFoundError, json.JSONDecodeError):
            self.tasks = []  # Если файл не найден или пустой, инициализируем пустой список

    # Метод для сохранения задач в файл
    def save_tasks(self):
        with open(self.filename, "w") as f:
            json.dump([t.to_dict() for t in self.tasks], f, indent=4)  # Сохраняем задачи в формате JSON

    # Метод для добавления новой задачи в хранилище
    def add_task(self, task: Task):
        self.tasks.append(task)
        self.save_tasks()

    # Метод для удаления задачи по ID
    def delete_task(self, task_id: int):
        self.tasks = [t for t in self.tasks if t.id != task_id]  # Фильтруем задачи, удаляя выбранную
        self.save_tasks()

    # Метод для обновления информации о задаче
    def update_task(self, updated: Task):
        for i, t in enumerate(self.tasks):
            if t.id == updated.id:  # Ищем задачу по ID
                self.tasks[i] = updated  # Заменяем старую задачу на обновлённую
        self.save_tasks()

    # Метод для получения всех задач
    def get_all_tasks(self):
        return self.tasks


# Основной класс для управления задачами
class TaskManager:
    def __init__(self):
        self.repo = TaskRepository()  # Создаём репозиторий для работы с задачами

    # Метод для создания новой задачи
    def create_task(self):
        title = input("Название: ")  # Вводим название задачи
        desc = input("Описание: ")  # Вводим описание задачи
        category = input("Категория: ")  # Вводим категорию задачи
        due = input("Срок (YYYY-MM-DD): ")  # Вводим срок выполнения задачи
        priority = input("Приоритет (low/medium/high): ")  # Вводим приоритет задачи
        task = Task(title, desc, category, due, priority)  # Создаём задачу
        self.repo.add_task(task)  # Добавляем задачу в репозиторий

    # Метод для отображения всех задач
    def list_tasks(self):
        tasks = self.repo.get_all_tasks()  # Получаем все задачи из репозитория
        if not tasks:
            print("Нет задач.")  # Если задач нет, выводим сообщение
            return
        print("\nВаши задачи:")
        for t in tasks:
            # Если задача выполнена, показываем зелёную галочку (✔), иначе красный крестик (✘)
            status = "✔" if t.is_completed else "✘"
            print(f"{t.id}. [{status}] {t.title} ({t.priority}) — до {t.due_date} | {t.category}")

    # Метод для завершения задачи
    def complete_task(self):
        task_id = int(input("ID задачи для завершения: "))  # Вводим ID задачи для завершения
        for task in self.repo.get_all_tasks():
            if task.id == task_id:  # Находим задачу по ID
                task.mark_complete()  # Отмечаем задачу как выполненную
                self.repo.update_task(task)  # Обновляем задачу в репозитории
                print(f"Задача {task_id} отмечена как выполненная!")
                break

    # Метод для удаления задачи
    def delete_task(self):
        task_id = int(input("ID задачи для удаления: "))  # Вводим ID задачи для удаления
        self.repo.delete_task(task_id)  # Удаляем задачу из репозитория
        print(f"Задача {task_id} удалена.")

    # Метод для запуска программы
    def run(self):
        while True:
            # Главное меню
            print("\n1. Добавить\n2. Показать\n3. Завершить\n4. Удалить\n5. Выход")
            choice = input("Выбор: ")
            if choice == "1":
                self.create_task()  # Добавить задачу
            elif choice == "2":
                self.list_tasks()  # Показать все задачи
            elif choice == "3":
                self.complete_task()  # Завершить задачу
            elif choice == "4":
                self.delete_task()  # Удалить задачу
            elif choice == "5":
                break  # Выход из программы
            else:
                print("Неверный ввод")  # Обработка неверного ввода

# Запуск программы
if __name__ == "__main__":
    manager = TaskManager()  # Создаём экземпляр TaskManager
    manager.run()  # Запускаем программу