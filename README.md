# Публикация комиксов

Cкрипт скачивает случайный комикс с сайта xkcd.com и публикует постом в сообществе Вконтакте.

### Как установить

Для взаимодействия с API Вконтакте, нужен ключ доступа пользователя. Для этого нужно создать приложение на странице "Вконтакте для разработчиков" по ссылке: https://vk.com/apps?act=manage. После создания приложения, нажимаем на кнопку "Редактировать". В адресной строке вы увидите ID, который необходимо записать, в созданный в папке проекта файл .env, следующим образом:
```
CLIENT_ID=Some_ID
```

Затем необходимо получить токен. Для этого необходимо перейти по ссылке, указав в параметре client_id ваш ID.
```
https://oauth.vk.com/authorize?client_id=0000000&display=page&scope=photos,groups,wall,offline&response_type=token&v=5.95
```
В адресной строке вы увидите токен следующего вида:
```
af545f7gfdsfg6c374c6749551e0efef231ec89b17190f5d0aa44a58606ertgrega0c89b41906gwec
```
Токен, записываем в файл .env:
```
ACCESS_TOKEN=af545f7gfdsfg6c374c6749551e0efef231ec89b17190f5d0aa44a58606ertgrega0c89b41906gwec
```
Также в .env файл записываем ID группы, где будет происходить постинг:
```
GROUP_ID=000000000
```
Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
### Пример использования
```
(env) iMac-Andrej:posting_vk anderskate$ python main.py 
Downloaded comic
Got server address
Uploaded comic to the server
Saved photo comic in the album group
Published comic
(env) iMac-Andrej:posting_vk anderskate$ 

```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).