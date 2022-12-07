import psycopg2
import json
from fastapi import FastAPI
import uvicorn


connection = psycopg2.connect(
    user="postgres",
    password="postgres",
    host="postgres",
    port="5432",
    database="postgres"
)

connection.autocommit = True
cursor = connection.cursor()


def init_db(file_path: str):
    sql_users = '''CREATE TABLE IF NOT EXISTS Users (
                   id SERIAL PRIMARY KEY,
                   name varchar(255),
                   last_name varchar(255),
                   time_created int,
                   gender varchar(255),
                   age varchar(255),
                   city varchar(255),
                   birth_day varchar(255),
                   premium BOOL,
                   ip varchar(255),
                   balance float4)
                   ;'''

    sql_insert = 'INSERT INTO users ({}) VALUES ({})'
    cursor.execute(sql_users)
    with open(file_path, 'r') as f:
        data = list(map(json.loads, f))
        for user in data:
            n_user = {k: v for k, v in user.items() if v is not None}
            res_keys = str(list(n_user.keys())).strip("[]").replace("'", '')
            res_val = str(list(n_user.values())).strip("[]")
            cursor.execute(sql_insert.format(res_keys, res_val))
        print('Inserted')


def create_tables():
    sql_createBets = '''CREATE TABLE IF NOT EXISTS Bets (
    id SERIAL PRIMARY KEY,
    date_created int,
    userId int REFERENCES users(id),
    eventId int REFERENCES events(id) );'''
    sql_createEvents = '''CREATE TABLE IF NOT EXISTS Events (
    id SERIAL PRIMARY KEY,
    type varchar(255),
    name varchar(255),
    event_date varchar(255) );'''
    cursor.execute(sql_createEvents)
    print("Table Events Created")
    cursor.execute(sql_createBets)
    print("Table Bets Created")


file = 'data.jsonl'
init_db(file)
app = FastAPI()
create_tables()


@app.get("/users")
def get_users():
    query = "SELECT row_to_json(users) FROM users"
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except:
        return "Cannot fetch all users"

@app.get("/user")
def get_users(id):
    query = 'SELECT * FROM users WHERE id = {}'.format(id)
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except:
        return "Cannot get user"



@app.delete("/user")
def delete_user(id):
    query = "DELETE FROM users WHERE id = {}".format(id)
    try:
        cursor.execute(query)
        return "Deleted user with id {}".format(id)
    except:
        return "Cannot delete user with id"


@app.put("/user")
def update_user(id, val):
    query = "UPDATE users SET {} WHERE id = {}".format(val, id)
    try:
        cursor.execute(query)
        return "updated {} in user with id {}".format(val, id)
    except:
        return "Cannot update user with id"


@app.post("/user")
def create_user(col, val):
    query = "INSERT INTO users ({}) VALUES  ({}) ".format(col, val)
    try:
        cursor.execute(query)
        return "created user {}".format(val)
    except:
        return "Something went wrong when creating new user"


@app.get("/bets")
def get_bets():
    query = "SELECT * FROM bets"
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except:
        return "Cannot get all bets"


@app.get("/bet")
def get_bet(id):
    query = 'SELECT * FROM bets WHERE id = {}'.format(id)
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except:
        return "Cannot get bet"


@app.delete("/bet")
def delete_bet(id):
    query = "DELETE FROM bets WHERE id = {}".format(id)
    try:
        cursor.execute(query)
        return "Deleted bet with id {}".format(id)
    except:
        return "Cannot delete bet with id"


@app.put("/bet")
def update_bet(id, val):
    query = "UPDATE bets SET {} WHERE id = {}".format(val, id)
    try:
        cursor.execute(query)
        return "updated {} in bet with id {}".format(val, id)
    except:
        return "Cannot update bet with id"


@app.post("/bet")
def create_bet(col, val):
    query = "INSERT INTO bets ({}) VALUES  ({}) ".format(col, val)
    try:
        cursor.execute(query)
        return "created bet {}".format(val)
    except:
        return "Something went wrong when creating new bet"


@app.get("/events")
def get_events():
    query = "SELECT * FROM events"
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except:
        return "Cannot get all events"


@app.get("/event")
def get_events(id):
    query = 'SELECT * FROM events WHERE id = {}'.format(id)
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except:
        return "Cannot fetch user with id"


@app.delete("/event")
def delete_events(id):
    query = "DELETE FROM events WHERE id = {}".format(id)
    try:
        cursor.execute(query)
        return "Deleted event with id {}".format(id)
    except:
        return "Cannot delete user with id"


@app.put("/event")
def update_events(id, val):
    query = "UPDATE events SET {} WHERE id = {}".format(val, id)
    try:
        cursor.execute(query)
        return "updated {} in bet with id {}".format(val, id)
    except:
        return "Cannot update event with id"


@app.post("/event")
def create_events(col, val):
    query = "INSERT INTO events ({}) VALUES  ({}) ".format(col, val)
    try:
        cursor.execute(query)
        return "created event {}".format(val)
    except:
        return "Something went wrong when creating new event"


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
