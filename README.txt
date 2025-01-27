## Executando o Projeto Local

1. Clone o repositório
2. Instale as dependências: `pip install -r requirements.txt`
3. Configure o banco de dados no `settings.py`
4. Execute as migrações: `python manage.py migrate`
5. Popule o banco: `python manage.py populate_db`
6. Inicie o servidor: `python manage.py runserver`

Build Docker:
docker-compose down -v
docker-compose up --build -d
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

Realizar testes Docker:
docker-compose run --rm web python manage.py test wallet_api_django2.tests.withdraw_test
docker-compose run --rm web python manage.py test wallet_api_django2.tests.user_test
docker-compose run --rm web python manage.py test wallet_api_django2.tests.wallet_test
docker-compose run --rm web python manage.py test wallet_api_django2.tests.transactions_test

## Endpoints
- POST /api/transfer/ - Realiza transferência
- GET /api/transactions/ - Lista transações com filtro de datas (start_date & end_date)