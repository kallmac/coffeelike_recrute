import pandas as pd
import os


def add_row_to_excel(file_path, new_row):
    # Проверяем, существует ли файл
    if not os.path.exists(file_path):
        # Если файл не существует, создаем новый DataFrame и сохраняем его
        df = pd.DataFrame(columns=new_row.keys())
        df.to_excel(file_path, index=False, engine='openpyxl')

    # Читаем существующий Excel файл
    df = pd.read_excel(file_path, engine='openpyxl')

    # Создаем DataFrame из новой строки (словаря)
    new_data = pd.DataFrame([new_row])

    # Добавляем новую строку к существующему DataFrame
    df = pd.concat([df, new_data], ignore_index=True)

    # Сохраняем обновленный DataFrame обратно в Excel файл
    df.to_excel(file_path, index=False, engine='openpyxl')


# Пример использования
if __name__ == "__main__":
    # Путь к вашему Excel файлу
    excel_file = 'data.xlsx'

    # Новая строка, которую нужно добавить (словарь)
    new_row_data = {
        'Имя': 'Сергей',
        'Возраст': 28,
        'Город': 'Москва'
    }
    new_row_data_2 = {
        'Имя': 'Денис',
        'Возраст': 16,
        'Город': 'Саров'
    }

    # Добавляем новую строку в Excel файл
    add_row_to_excel(excel_file, new_row_data)
    add_row_to_excel(excel_file, new_row_data_2)
