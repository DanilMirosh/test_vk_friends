Необходимо спроектировать и разработать Django-сервис друзей.
Сервис должен предоставлять возможности:
-зарегистрировать нового пользователя
-оправлять одному пользователю заявку в друзья другому
-принять/отклонить пользователю заявку в друзья от другого пользователя
-посмотреть пользователю список своих исходящих и входящих заявок в друзья
-посмотреть пользователю список друзей
-получать пользователю статус дружбы с каким-то другом пользователем (нет ничего/есть исходящая заявка/есть входящая заявка/ уже друзья)
-удалить пользователю другого пользователя из своих друзей
-если пользователь 1 отправляет заявку в друзья пользователю 2, а пользователь 2 отправляет заявку пользователю 1, то они автоматически становятся друзьями, их заявки автоматом принимаются.

Модель пользователя может быть самой простой:
- id
-username

Необходимо:
-описать REST интерфейс сервиса с помощью OpenAPI
-написать на Django сервис по этой спецификации
-описать краткую документацию с примерами запуска сервиса и вызова его API
+unit-тесты будут плюсом
+Dockerfile для упаковки в контейнер будет плюсом

Входные артефакты:
-исходный код
-OpenAPI спецификация
- документация с описанием запуска и примерами использования API