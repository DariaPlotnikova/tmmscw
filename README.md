...

1) 
установить cloud_sql_proxy
chmod +x cloud_sql_proxy

2)
gcloud sql instances describe tmdb
./cloud_sql_proxy --instance="tmmosc-1383:asia-northeast1:tmdb"=tcp:3306

3)
запустить proxy локально: ./cloud_sql_proxy -instances=tmmosc-1383:asia-northeast1:tmdb=tcp:3306
(потребует credentials, тогда делаем - gcloud beta auth application-default login, выбираем свой гугл-аккаунт; повторяем запуск proxy)
(источник, подключение к sql - https://cloud.google.com/sql/docs/postgres/connect-external-app#proxy)

должны увидеть:
(env) daria@dariaplotnikova:~/tmmosc$ ./cloud_sql_proxy -instances=tmmosc-1383:asia-northeast1:tmdb=tcp:3306
2017/10/19 11:44:14 Listening on 127.0.0.1:3306 for tmmosc-1383:asia-northeast1:tmdb
2017/10/19 11:44:14 Ready for new connections

4)
./manage.py makemigrations
./manage.py migrate

5) 
./manage.py runserver 0.0.0.0:55


## Подключение к psql-клиенту локально

1) Установить postgres-client (если не установлен): ``sudo apt-get install postgresql-client``

2) Подключиться к клиенту:

```
psql 'host=127.0.0.1 port=3306 sslmode=disable dbname=postgres user=postgres'
```
Здесь порт, имя базы данных и пользователь берутся из настройки settings.DATABASES

## Патчи

1) Очистка всех таблиц приложения
```
begin;
drop schema public cascade;
create schema public;
commit;
```


==================================================================
Соревнование
	название
	дата начала
	дата конца
	дата окончания предварительной заявки
	место центра соревнований (строка+карта)
	место центра X
	место центра Y


День соревнования
	FK на сореву
	техническая инфа (документ)
	дата
	место старта (строка)
	место старта X
	место старта Y
	дата и время окончания подачи технической заявки


Дистанция дня
	FK на день
	тип (личка/связка/...)
	длина
	класс
	набор высоты
	кол-во этапов
	допустимые возраста (мультиселект)
	допустимые разряды (мультиселект)
	пол


Пользователь (как регать юзеров? Как привязать гугл/вк/фб-аккаунт?)
	уникальный ID
	email
	год рождения
	разряд
	пароль редактирования аккаунта
	привязка к аккаунтам
	участник?
	рукль?
	орг?
	активирован?

Команда
	название
	территория



Участник-команда
	FK команды
	FK участника
	дата создания записи
	FK на кто создал

Рукль-команда
	FK команды
	FK рукля
	дата создания записи



ВОПРОСЫ:
	у одного рукля может быть только 1 команда?
	у одной команды может быть только 1 рукль? да
	один участник может состоять в нескольких командах, но при заявке на ДЕНЬ соревы - только один рукль (=1 команда) может его заявить от себя, для остальных и для самого участника блокировать (пока)


ЛОГИКА:
	При регистрации руклем участников на соревы:
	Вверху страницы должна быть надпись "Если ваш участник состоит в нескольких коллективах, то при заявке будет указана ваша команда. Другие руководители не смогут повторно заявить участника на один и тот же день, что и вы."

	по каждому выводится в подсказку-попап "участник состоит в N коллективах - Команда 1, Команда 2, Команда N"


	При регистрации на соревы руководителем, если человек с такими ФИО и годом рождения уже зареган на старт, то выводится предупреждение:
	"Такой человек уже зареган на старт под командой Команда 1. Он состоит в N коллективах - Команда 1, команда 2, ... команда N. Вы не можете заявить этого участника дважды. Обратитель к руководителю Команды 1."


	При регистрации на сореву участником, если его уже кто-то зарегал, выводить "Вас зарегистрировал руководитель команды Команда 1. Вы не можете изменить свою команду (это пока)"


день - неск дисциплин+неск классов


Все рукли при регистрации.
В команде есть галка "я личник, не регистрировать команду"
После авторизации отправляется письмо с ключом активации

Если юзер хочет роль организатора, то он связыватеся в админом и тот выставляет ему роль.







