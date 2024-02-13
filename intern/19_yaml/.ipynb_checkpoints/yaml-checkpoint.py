import yaml
from typing import Dict

def yaml_to_env(config_file: str) -> str:
    # Открываем YAML файл для чтения
    with open(config_file, 'r') as file:
        # Загружаем данные из YAML файла
        config_data = yaml.safe_load(file)

    # Вспомогательная функция для "расплющивания" вложенного словаря в плоский список пар ключ-значение
    def flatten_dict(d, parent_key='', sep='.'):
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            # Если значение является словарем, рекурсивно вызываем flatten_dict
            if isinstance(v, dict):
                items.extend(flatten_dict(v, new_key, sep=sep).items())
            else:
                # Добавляем пару ключ-значение в список
                items.append((new_key, v))
        return dict(items)

    # Преобразуем вложенный словарь в плоский список пар ключ-значение
    flat_config = flatten_dict(config_data)
    # Формируем строку переменных окружения, разделяя каждую пару ключ-значение символом переноса строки
    env_str = '\n'.join([f"{key}={value}" for key, value in flat_config.items()])
    return env_str  # Возвращаем строку переменных окружения


def env_to_yaml(env_list: str) -> str:
    # Инициализация пустого словаря, который будет содержать переменные окружения
    env_dict = {}
    
    # Проход по каждой строке в списке строк env_list
    for line in env_list.split('\n'):
        # Проверяем, содержит ли строка что-то, кроме пробельных символов
        if line.strip():
            # Разделяем строку на ключ и значение по первому символу "="
            key, value = line.split('=', 1)
            # Добавляем пару ключ-значение в словарь, удаляя лишние пробелы с обеих сторон
            env_dict[key.strip()] = value.strip()

    # Вспомогательная функция для преобразования плоского словаря во вложенный
    def unflatten_dict(d, sep='.'):
        result = {}
        for key, value in d.items():
            # Разбиваем ключ на части по разделителю (по умолчанию ".")
            parts = key.split(sep)
            current = result
            # Проходим по каждой части ключа, создавая вложенные словари при необходимости
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]
            # Устанавливаем значение для последней части ключа
            current[parts[-1]] = value
        return result

    # Преобразовываем плоский словарь во вложенный и затем в формат YAML
    yaml_data = yaml.dump(unflatten_dict(env_dict), default_flow_style=False)
    return yaml_data
