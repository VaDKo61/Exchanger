# Exchanger

Платформа для обмена вещами (бартерная система).

# Установка

1. Клонируйте репозиторий

        git clone https://github.com/VaDKo61/Exchanger

2. Запустите контейнер в Docker
    
        cd .\Exchanger\
        docker compose up --build

3. Запустите миграцию

        cd .\Exchanger\
        docker compose exec exchanger python manage.py migrate

4. Создайте суперюзера

        docker compose exec exchanger python manage.py createsuperuser

5. Авторизуйтесь по ссылке 

        http://127.0.0.1:8000/admin

6. Документаци API

        http://127.0.0.1:8000/swagger/

7. Запуск тестов

         cd .\exchanger\
         pip install -r requirements.txt
         python manage.py test
         


        


