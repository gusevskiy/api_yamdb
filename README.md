![YamDB](img/logo.png)
# YaMDb
![python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue) ![django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green) ![drf](https://img.shields.io/badge/django%20rest-ff1709?style=for-the-badge&logo=django&logoColor=white) ![jwt](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=JSON%20web%20tokens&logoColor=white)  
YaMDb - сервис, позволяющий писать и читать отзывы на фильмы, книги, картины и т.д.
## Как поднять у себя?
```py
# Клонируем репозиторий
git clone https://github.com/gusevskiy/api_yamdb
cd api_yamdb
# Создаём виртуальное окружение (venv)
python -m venv venv
./venv/Scripts/Activate
# Загружаем все нужные библитеки
pip install -r requirements.txt
# Выполняем миграции и запускаем проект
python manage.py migrate
python manage.py runserver
```
## Как пользоваться?
Этот репозиторий - бекенд проекта YaMDb, поэтому здесь есть API. Вот как можно зарегистрироваться и написать отзыв.
1. Отправляем POST запрос на эндпоинт /auth/signup/, передавая почту и имя пользователя в тело запроса, например:
```json
{
    "email": "bestreviewer152@yandex.ru",
    "username": "bestreviewer"
}
```
2. После этого на почту должен прийти код подтверждения, копируем его и отправляем POST запрос на эндпоинт /auth/token/, передавая имя пользователя и код подтверждения в тело запроса, например:
```json
{
    "username": "bestreviewer",
    "confirmation_code": "71fdf3ab"
}
```
3. Получаем JWT токен, в заголовках следующих запросов добавляем `Authorization: Bearer ТОКЕН_ПОЛЬЗОВАТЕЛЯ` .
4. Читаем документацию и спокойно пользуемся сервисом. :)
5. первый эндпойнт http://0.0.0.0:8000/api/v1/ выведет варианты 
6. Заполнитьь БД тестовыми данными можно командой 
   ```{bash}
   python3 manage.py load_csv_data
   ```