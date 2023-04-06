
Завдання:

1. Створити базу даних Postgres, використовуючи docker compose, разом з існуючою API.

2. Інтегрувати БД в API. CRUD операції повинні працювати з базою, а не з data.jsonl файлом. Створити необхідну таблицю, вказати всі необхідні колонки, типи, схему. Здійснити INSERT даних, наявних в data.jsonl у таблицю. Таблицю можна назвати Users. Схема цієї таблиці:

- id

- name

- last_name

- time_created

- gender

- age

- city

- birth_day

- premium

- ip

На роботу ендпойнтів це ніяк не повинно вплинути. FastAPI має детальну документацію, як здійснити інтеграцію з базою даних: https://fastapi.tiangolo.com/tutorial/sql-databases/ (sqlalchemy + pydantic packages)

3. Додати 2 нові таблиці: Bets та Events.

Таблиця Bets повинна містити наступні колонки:

- id

- date_created

- userId

- eventId

Таблиця Events повинна містити наступні колонки:

- id

- type (ex. football, basketball etc.)

-name (ex. Spain - Germany)

- event_date

4. Створити CRUD ендпойнти для роботи з цими двума таблицями з відповідними валідаціями. Наприклад: неможливо створити bet з userId, котрого не існує.

5. Запити до бази даних писати, використовуючи SQL, без використання ORM.
