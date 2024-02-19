class DataProcessor:
    def __init__(self, data):
        '''
        Инициализация экземпляра класса DataProcessor.

        Parameters:
        data (list): Набор данных для обработки.
        '''
        self.data = data
        self.processed_data_ = None

    def process(self):
        '''
        Функция предобработки данных.

        Вычисляет отклонение от среднего для каждого элемента набора данных.
        Результат сохраняется в атрибут processed_data_.
        '''
        n = len(self.data)
        mean = sum(self.data) / n
        result = list(map(lambda x: x - mean, self.data))
        self.processed_data_ = result

    def save_to_file(self, name):
        '''
        Функция сохранения обработанных данных в файл.

        Если данные были предварительно обработаны (process вызван), сохраняет
        обработанные данные в указанный файл. Каждый элемент обработанных данных
        сохраняется на отдельной строке.

        Parameters:
        name (str): Имя файла для сохранения данных.
        '''
        if self.processed_data_:
            with open(name, 'w', encoding='utf-8') as file:
                for elem in self.processed_data_:
                    file.write(f"{elem}\n")

# Example of usage
processor = DataProcessor(data=[1, 2, 3, 4, 5])
processor.process()
processor.save_to_file("processed_data.txt")
