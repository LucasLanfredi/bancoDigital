# Projeto Wallet API

## Descrição
Uma API para gerenciar transações financeiras, incluindo autenticação de usuários, saldo de carteira, depósitos, saques e transferências.

## Executando o Projeto Local
1. Clone o repositório
2. Instale as dependências: `pip install -r requirements.txt`
3. Configure o banco de dados no `settings.py`
4. Ececute os mapeamentos: `python manage.py makemigrations`
5. Execute as migrações: `python manage.py migrate`
6. Popule o banco: `python manage.py populate_db`
7. Inicie o servidor: `python manage.py runserver`

## Build Docker:
1. Configure o banco de dados no `settings.py`
2. docker-compose down -v
3. docker-compose up --build -d
4. docker-compose exec web python manage.py makemigrations
5. docker-compose exec web python manage.py migrate

Realizar testes Docker:
docker-compose run --rm web python manage.py test wallet_api_django2.tests.withdraw_test
docker-compose run --rm web python manage.py test wallet_api_django2.tests.user_test
docker-compose run --rm web python manage.py test wallet_api_django2.tests.wallet_test
docker-compose run --rm web python manage.py test wallet_api_django2.tests.transactions_test

## Endpoints
Autenticação
POST /api/auth/register/ - Registra um novo usuário.
POST /api/auth/login/ - Realiza o login de um usuário.

Carteira
GET /api/wallets/balance/ - Retorna o saldo atual da carteira do usuário autenticado.
POST /api/wallets/deposit/ - Adiciona fundos à carteira do usuário.
POST /api/wallets/withdraw/ - Realiza um saque da conta do usuário.

Transações
POST /api/transfer/ - Realiza uma transferência de valores entre usuários.
GET /api/transactions/ - Retorna a lista de transações do usuário autenticado passando um prazo de filtro.
