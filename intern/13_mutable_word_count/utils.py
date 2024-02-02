def word_count(batch, count=None):
    '''
    Функция принимает на вход текстовые батчи и выдает словарь с количеством букв

    Вход
    batch: батч
    count: словарь
    '''
    if count is None:
        count = {}
    for text in batch:
        for word in text.split():
            count[word] = count.get(word, 0) + 1
    return count
    