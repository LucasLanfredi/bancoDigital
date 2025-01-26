

Build Docker:
docker-compose down -v
docker-compose up --build -d
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

Realizar testes Docker:
docker-compose run --rm web python manage.py test wallet_api_django2.tests.withdraw_test
docker-compose run --rm web python manage.py test wallet_api_django2.tests.user_test
docker-compose run --rm web python manage.py test wallet_api_django2.tests.wallet_test