# Задание
Вашей задачей является создание класса Python для обработки данных DataProcessor. 

Вам следует определить атрибуты, такие как data и processed_data_.

Напишите метод под названием process, который не принимает параметры.

Этот метод должен реализовать логику предобработки данных и сохранить результат в атрибут processed_data_.

Предобработка следующая: Необходимо вычислить отклонение от среднего. Для всего набора данных data вычислить среднее арифметическое и для каждого значения вычислить 
x_i − x_mean
​
и сохранить в processsed_data_.

Напишите метод save_to_file, который принимает имя файла в качестве параметра и сохраняет обработанные данные в указанный файл. 

Каждое значение в списке processed_data_ необходимо сохранять на отдельной строке. 

Если данные не были обработаны, файл сохранять не нужно.