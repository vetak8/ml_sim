Наша модель динамического ценообразования на маркетплейсе KarpovExpress предсказывает оборот на завтра в рублях.
Прогноз выполняется на основе некоторого набора фичей и цены. 
Также мы знаем, сколько товаров хранится на складе и доступно для продажи.
Предполагается, что на данные товары нет никаких дополнительных промоакций, скидок и для каждого покупателя цена одинакова.

Колонки таблицы
sku – SKU (Stock Keeping Unit), уникальный ID товара (тип int)
gmv – GMV (Gross Merchandise Volume), аналог розничного товарооборота (тип float)
stock – число единиц товара на складе (тип int)
price – цена на товар (тип float)
Формула расчёта: GMV = (цена) * (штук продано)

Необходимо написать функцию для постобработки предсказаний модели

На входе:
| sku | gmv | price | stock |
—————————————————————————————
| 100 | 400 |   100 |     3 |
| 200 | 350 |    70 |    10 |
| 300 | 500 |   120 |     5 |

На выходе:
| sku | gmv | price | stock |
—————————————————————————————
| 100 | 300 |   100 |     3 |
| 200 | 350 |    70 |    10 |
| 300 | 480 |   120 |     5 |