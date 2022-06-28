# Yandex REST API
(Django + Django Rest Framework + PostgresQL)

Репозиторий с реализацией тестового задания для Школы Бэкенда 2022.
Приложение представляет собой веб-интерфейс позволящий добавлять, изменять товары, разделять их по категориям, получать статистику изменений товара.

**Эндпоинты**

POST: /imports
Публикация списка товаров/категорий

GET: /nodes/{id}
Получения информации об элементе и о его дочерних элементах

DELETE: /delete/{id}
Удаление элемента

GET: /sales
Получение списка товаров, цена которых изменилась в сутки перед указанной датой

GET: /nodde/{id}/statistic
Получение истории изменения товара/категории.
Реализовано с использованием библиотеки django-simple-history

**Код**

Все необходимые контроллеры, модели, функции, маршрутизаторы находятся в папке service. 
Views.py содержат пять контроллеров, которые и отвечают на запросы, полученные приложением. 
Разнообразные вспомогательные функции расположены в utils.py. Такие, как проверки запросов, дат, корректности uuid. Так же, файл serializers.py содержит функцию сериализатор, используемую для возвращения информации о товарах.

Все эндпоинты покрыты юнит-тестами, содержащимися в файле unit_test.py. Оригинальный файл был расширен тестами для sales, node/statistic. Так же добавлены дополнительные тесты для imports.

**Запуск**

Для запуска проекта необходимо склонировать репозиторий к себе, установить PostgresQL, создать новую базу данных и указать её данные в settings.py.
Так же проект развернут в контейнере docker и доступен по адресу http://10.22.3.234/ (Через VPN).

**Работа**

Сервис способен обрабатывать несколько запросов одновременно.

№UPD: Позорный баг
Обнаружил баг с форматом даты в коде, из-за чего миллисекунды приравниваются к секундам, из-за некорреткногй строки форматирования, что влечет за собой ошибочные даты при ненулевых секундах. Последний коммит исправляет исключительно этот баг.

