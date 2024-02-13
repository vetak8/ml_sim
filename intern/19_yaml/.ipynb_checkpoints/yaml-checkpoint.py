import yaml

def yaml_to_env(config_file: str) -> str:
    # # Открываем YAML файл для чтения
    # with open(config_file, 'r') as config_file:
    #     # Загружаем данные из YAML файла
    config_data = yaml.safe_load(config_file)

    # Вспомогательная функция для "расплющивания" вложенного словаря в список пар ключ-значение
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
    # Формируем строку переменных окружения, разделяя пару ключ-значение символом переноса строки
    env_str = '\n'.join([f"{key}={value}" for key, value in flat_config.items()])
    return env_str  # Возвращаем строку переменных окружения


import yaml

def env_to_yaml(env_list: str) -> str:
    # Инициализация пустого словаря, который будет содержать переменные окружения
    env_dict = {}

    # Проход по каждой строке в списке строк env_list
    for line in env_list.split('\n'):
        # Проверяем, содержит ли строка что-то, кроме пробельных символов
        if line.strip():
            # Разделяем строку на ключ и значение по первому символу "="
            key, value = line.split('=', 1)
            # Преобразуем числовые значения в числа
            if value.isdigit():
                value = int(value)
            elif '.' in value and all(part.isdigit() for part in value.split('.')):
                value = float(value) 
            elif value.lower() == 'true':
                value = True
            elif value.lower() == 'false':
                value = False
            # Добавляем пару ключ-значение в словарь, удаляя лишние пробелы с обеих сторон
            env_dict[key.strip()] = value

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

    # Преобразуем плоский словарь во вложенный и затем в формат YAML
    yaml_data = yaml.dump(unflatten_dict(env_dict), default_flow_style=False, default_style=None)
    return yaml_data
