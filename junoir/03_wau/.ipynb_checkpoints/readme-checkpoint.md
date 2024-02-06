## WAU

Вам предоставлен доступ к таблице default.churn_submits. 
В ней находятся данные по активности пользователей нашего Симулятора. 
Одна строка = одна попытка решения каким-то студентом какой-то задачи. 

churn_submits состоит из колонок: 

submit_id – id события-попытки
timestamp – время попытки
user_id  – id пользователя
task_id  – id задания
submit – номер попытки
score – балл за задание
is_solved – решил/не решил
### Задание
1. Напишите запрос с расчётом WAU за весь период скользящим окном в неделю с шагом в 1 день, при этом текущая дата должна включаться в расчет.

<picture>
 <source media="(prefers-color-scheme: dark)" srcset="https://github.com/vetak8/ml_sim/blob/main/junoir/03_wau/wau.png">
 <source media="(prefers-color-scheme: light)" srcset="https://github.com/vetak8/ml_sim/blob/main/junoir/03_wau/wau.png">
 <img alt="YOUR-ALT-TEXT" src="https://github.com/vetak8/ml_sim/blob/main/junoir/03_wau/wau.png">
</picture>
