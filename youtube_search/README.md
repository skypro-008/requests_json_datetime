# YouTube поиск

Программа выполняет поиск видео на YouTube по заданному запросу и выводит список видео 
с наибольшим соотношением количества лайков к количеству просмотров.

## Запуск

1. Получите ключ API YouTube, следуя инструкциям на [этой странице](https://developers.google.com/youtube/registering_an_application)
2. Установите ключ API в переменную окружения `YT_API_KEY`
3. Запустите скрипт

## Использование

1. Запустите `main.py`
2. Введите поисковый запрос в консоль
3. После того как результаты поиска будут выведены в консоль, выберите одну из доступных опций
   - Ввести новый запрос
   - Сохранить результаты в файл JSON и ввести новый запрос
   - Сохранить результаты в файл JSON и выйти
   - Выйти