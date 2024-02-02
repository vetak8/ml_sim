Мы занимаемся динамическим ценообразованием и хотим, чтобы наша модель учитывала цены конкурентов. Пусть для каждого товара (sku) у нас имеется base_price – наша текущая цена. На каждый наш товар благодаря команде матчинга найдены 1, несколько или ни одной цен конкурентов – они записаны в колонке comp_price. Конкуренты имеют приоритет (колонка rank), причём в рангах могут быть пропуски (либо -1, если не найдено ни одной цены конкурента).

Поскольку может быть найдено несколько цен конкурентов, их необходимо согласно какому-то правилу агрегировать. В колонке agg указан тип агрегации:

avg – берем среднее
med – медиану
min – минимальную цену
max – максимальную
rnk – цену конкурента, имеющего наибольший приоритет (наименьший ранг)
После агрегации мы записываем агрегированную цену конкурента в колонку comp_price.

Осталось определиться, какую брать финальную цену new_price:

если для товара цен конкурентов не найдено, оставляем старую цену
если агрегированная цена конкурента отличается не более чем на ± 20% от старой цены, ставим её, иначе оставляем старую
Описание решения
Напишите функцию agg_comp_price, которая на вход принимает датафрейм, группирует его по полю sku, вариант группировки указан в поле agg (Для одинаковых sku, agg одинаковые).

Решение должно быть отсортировано по sku, а индекс начинаться с 0 и быть последовательным.