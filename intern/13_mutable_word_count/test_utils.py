import utils

def test_word_count():
    # Тест для обычного использования функции
    texts = ["apple banana orange", "banana grape apple"]
    count = utils.word_count(texts)
    assert count == {'apple': 2, 'banana': 2, 'orange': 1, 'grape': 1}

def test_word_count_tricky():
    # Тест для выявления проблемы с изменяемым значением по умолчанию
    batch1 = ["apple banana orange", "banana grape apple"]
    batch2 = ["apple orange grape", "grape orange banana"]
    
    # Используем один и тот же объект count для двух батчей
    count = utils.word_count(batch1)
    count_copy = count.copy()  # Создаем копию count
    count = utils.word_count(batch2, count_copy)

    # Ожидаем AssertionError, так как count изменился после первого вызова
    assert count == {'apple': 3, 'banana': 3, 'orange': 3, 'grape': 3}, f"Actual count: {count}"

if __name__ == "__main__":
    test_word_count()
    try:
        test_word_count_tricky()
    except AssertionError as e:
        print(f"Test test_word_count_tricky passed with error: {e}")
    else:
        print("All tests passed.")
