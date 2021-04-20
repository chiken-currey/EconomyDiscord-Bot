import sqlite3
import json
import random

conn = sqlite3.connect('data\\userdata.db')

c = conn.cursor()

'''
c.execute("""
CREATE TABLE members (
    _id integer(18) NOT NULL UNIQUE,

    _messages integer NOT NULL,
    _msgCool integer,

    _level integer NOT NULL,
    _xp integer NOT NULL,

    _money integer NOT NULL,
    _bank integer NOT NULL,
    _items integer NOT NULL,

    _job varchar(32),
    _jobWage integer NOT NULL,

    _eduLevel integer NOT NULL,
    _eduPoint integer NOT NULL,
    _eduCool integer,
    _eduQues varchar(128),
    _eduAnw BOOLEAN

    )
""")
'''

'''
c.execute("""
CREATE TABLE members (
    _id integer(18) NOT NULL,
    _name varchar(32) NOT NULL,
    _emoji varchar(32) NOT NULL,
    _price integer NOT NULL,
    _rarity FLOAT NOT NULL,
    _amount integer NOT NULL
    )
""")
'''

'''
c.execute('INSERT INTO _421717515614289950 VALUES (:id ,:name ,:emoji ,:price ,:rarity, :amount)',
{'id':0, 'name':'Mansion', 'emoji':':classical_building:', 'price':458779, 'rarity':0.21796987220426392, 'amount': 1})
'''

'''
for x in range(2000):
    first_name = random.choice(json.load(open('first-names.json')))
    last_name = random.choice(json.load(open('last-names.json')))
    pay = random.randint(0, 20000)
    c.execute(f'INSERT INTO employees VALUES ({x}, "{first_name}","{last_name}","{pay}")')
'''
'''
c.execute('SELECT _id FROM members')

for x in c.fetchall():
    print(x)
'''

c.execute("""UPDATE members SET _eduCool = NULL
WHERE _id = :d""",
{'d': 421717515614289950})


conn.commit()
conn.close()