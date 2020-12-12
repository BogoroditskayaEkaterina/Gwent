from config import auth
from sqlalchemy import Table, Column, Integer, String, MetaData, create_engine, func


engine = create_engine('postgresql+psycopg2://{}:{}@localhost/postgres'.format(auth['user'], auth['password']), echo=True)
cursor = engine.connect()

query = '''
CREATE OR REPLACE FUNCTION f_create_db(dbname text)
    RETURNS integer AS
$func$
BEGIN
IF EXISTS(SELECT 1 FROM pg_database WHERE datname = dbname) THEN
    RAISE NOTICE 'Database already exists';
ELSE
    PERFORM dblink_exec('dbname=postgres user=kate password=1234', 'CREATE DATABASE ' || quote_ident(dbname));
END IF;
RETURN 0;
END
$func$ LANGUAGE plpgsql;
'''
cursor.execute(query)
metadata = MetaData()

card_list = Table('cards', metadata,
                      Column('name', String, primary_key=True),
                      Column('position', String),
                      Column('fraction', String),
                      Column('power', Integer),
                      Column('ability', String))

card_abilities = Table('abilities', metadata,
                    Column('name', String, primary_key=True),
                    Column('description', String))

card_position = Table('fraction', metadata,
                    Column('name', String, primary_key=True),
                    Column('number', Integer))


def create_db(dbname):
    global cursor
    cursor.execute(func.f_create_db(dbname))
    cursor.close()
    string = 'postgresql+psycopg2://{}:{}@localhost/' + dbname
    engine = create_engine(string.format(auth['user'], auth['password']), echo=True)
    cursor = engine.connect()
    metadata.create_all(engine)


query1 = '''
insert into cards
values 
('Вернон Роше', 'Ближний бой', 'Северные королевства', 10, 'Невосприимчивость'),
('Ян Наталис', 'Ближний бой', 'Северные королевства', 10, 'Невосприимчивость'),
('Эстерад Тиссен', 'Ближний бой', 'Северные королевства', 10, 'Невосприимчивость'),
('Филиппа Эльхарт', 'Дальний бой', 'Северные королевства', 10, 'Невосприимчивость'),
('Реданский пехотинец', 'Ближний бой', 'Северные королевства', 1, 'нет'),
('Грёбаная пехтура', 'Ближний бой', 'Северные королевства', 1, 'Прочная связь'),
('Ярпен Зигрин', 'Ближний бой', 'Северные королевства', 2, 'нет'),
('Боец Синих Полосок', 'Ближний бой', 'Северные королевства', 4, 'Прочная связь'),
('Сигизмунд Дийкстра', 'Ближний бой', 'Северные королевства', 4, 'Шпион'),
('Принц Стеннис', 'Ближний бой', 'Северные королевства', 5, 'Шпион'),
('Зигфрид из Денесле', 'Ближний бой', 'Северные королевства', 5, 'нет'),
('Бьянка', 'Ближний бой', 'Северные королевства', 5, 'нет'),
('Шелдон Скаггс', 'Дальний бой', 'Северные королевства', 4, 'нет'),
('Сабрина Глевиссиг', 'Дальний бой', 'Северные королевства', 4, 'нет'),
('Рубайлы из Кринфрида', 'Дальний бой', 'Северные королевства', 5, 'Прочная связь'),
('Шеала де Тансервилль', 'Дальний бой', 'Северные королевства', 5, 'нет'),
('Кейра Мец', 'Дальний бой', 'Северные королевства', 5, 'нет'),
('Детмольд', 'Дальний бой', 'Северные королевства', 6, 'нет'),
('Каэдвенский осадный мастер', 'Осадные', 'Северные королевства', 1, 'Прилив сил'),
('Талер', 'Осадные', 'Северные королевства', 1, 'Шпион'),
('Лекарь Бурой Хоругви', 'Осадные', 'Северные королевства', 5, 'Медик'),
('Осадная башня', 'Осадные', 'Северные королевства', 6, 'нет'),
('Баллиста', 'Осадные', 'Северные королевства', 6, 'нет'),
('Требушет', 'Осадные', 'Северные королевства', 6, 'нет'),
('Катапульта', 'Осадные', 'Северные королевства', 8, 'Прочная связь')
'''

def insert_data_t1():
    cursor.execute(query1)

query2 = '''
insert into fraction values
('Северные королевства', 25),
('Нильфгаард', 5)
'''

def insert_data_t2():
    cursor.execute(query2)

query11 = '''
insert into abilities values
('Прочная связь', 'карты, имеющие эту способность, перемножают свою силу на количество своих побратимов в ряду'),
('Шпион', 'карта кладется на поле противника (сила карты прибавится к его очкам), взамен вы берете 2 карты из своей колоды'),
('Медик', 'возвращает одну карту из отбоя на стол'),
('Невосприимчивость', 'на такую карту не действуют никакие способности других карт'),
('Прилив сил', 'дает +1 к силе всем картам в ряду, кроме себя')
'''

def insert_data_t3():
    cursor.execute(query11)

def show_table(dbname):
    string = 'select * from ' + dbname
    temp = cursor.execute(string)
    return(list(temp))

query3 = '''
DROP FUNCTION IF EXISTS insert_card(text, text, text, bigint, text);
CREATE FUNCTION insert_card(a1 text, a2 text, a3 text, a4 bigint, a5 text)
RETURNS void
AS
$$
insert into cards values
(a1, a2, a3, a4, a5)
$$Language sql;
'''

def insert_card(a1, a2, a3, a4, a5):
    cursor.execute(query3)
    cursor.execute(func.insert_card(a1, a2, a3, a4, a5))

query4 = '''
CREATE OR REPLACE FUNCTION change_num_nk()
RETURNS trigger AS
$$
BEGIN
	UPDATE fraction SET number = number + 1 WHERE name = 'Северные королевства';
	RETURN NULL;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS upd_num ON cards;

CREATE TRIGGER upd_num AFTER INSERT ON cards
FOR EACH ROW EXECUTE PROCEDURE change_num_nk();
'''

query5 = '''
CREATE OR REPLACE FUNCTION delete_num_nk()
RETURNS trigger AS
$$
BEGIN
	UPDATE fraction SET number = number - 1 WHERE name = 'Северные королевства';
	RETURN NULL;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS upd_num2 ON cards;

CREATE TRIGGER upd_num2 AFTER DELETE ON cards
FOR EACH ROW EXECUTE PROCEDURE delete_num_nk();
'''

query6 = '''
create INDEX ability ON cards (ability);
'''


def load_triggers_index():
    cursor.execute(query4)
    cursor.execute(query5)
    cursor.execute(query6)


def clean_table(name):
    string = 'delete from ' + name
    cursor.execute(string)


query7 = '''
DROP FUNCTION IF EXISTS delete_card();
CREATE FUNCTION delete_card()
RETURNS void
AS
$$
DELETE FROM cards WHERE name = (SELECT name FROM cards ORDER BY name DESC LIMIT 1)
$$Language sql;
'''

def delete_card():
    cursor.execute(query7)
    cursor.execute(func.delete_card())

query8 = '''
DROP FUNCTION IF EXISTS search_ability(text);
CREATE FUNCTION search_ability(str text)
RETURNS text
AS
$$
select b.description
from cards as a, abilities as b 
WHERE a.ability=b.name AND a.name = str;
$$Language sql;
'''

def search_ability(name):
    cursor.execute(query8)
    temp = list(cursor.execute(func.search_ability(name)))
    return(temp)


query9 = '''
DROP FUNCTION IF EXISTS change_card(bigint, text);
CREATE FUNCTION change_card(new_power bigint, card_name text)
RETURNS void
AS
$$
UPDATE cards SET power = new_power where name = card_name ;
$$Language sql;
'''

def change_card(new_power, card_name):
    cursor.execute(query9)
    cursor.execute(func.change_card(new_power, card_name))

def show_base():
    print(list(cursor.execute('SELECT current_database()')))

query10 = '''
CREATE OR REPLACE FUNCTION f_drop_db(dbname text)
    RETURNS integer AS
$func$
BEGIN
IF EXISTS(SELECT 1 FROM pg_database WHERE datname = dbname) THEN
    PERFORM dblink_exec('dbname=postgres user=kate password=1234', 'DROP DATABASE ' || quote_ident(dbname));
ELSE
    RAISE NOTICE 'Database do not exists';
END IF;
RETURN 0;
END
$func$ LANGUAGE plpgsql;
'''

def delete_base(dbname):
    cursor.execute(query10)
    cursor.execute(func.f_drop_db(dbname))

def connect_postgres():
    global cursor
    cursor = engine.connect()

def close_base(dbname):
    string = "SELECT pg_terminate_backend(pg_stat_activity.pid) " + "FROM pg_stat_activity WHERE pg_stat_activity.datname = " + "'" + dbname + "'" + "AND pid <> pg_backend_pid();"
    cursor.execute(string)

query12 = '''
DROP FUNCTION IF EXISTS delete_chosen_card(text);
CREATE FUNCTION delete_chosen_card(card_name text)
RETURNS void
AS
$$
DELETE FROM cards WHERE name = card_name;
$$Language sql;
'''

def delete_chosen_card(name):
    cursor.execute(query12)
    cursor.execute(func.delete_chosen_card(name))

query13 = '''
DROP FUNCTION IF EXISTS delete_some_cards(bigint);
CREATE FUNCTION delete_chosen_card(del_power bigint)
RETURNS void
AS
$$
DELETE FROM cards WHERE power = del_power;
$$Language sql;
'''

def delete_some_cards(power):
    cursor.execute(query13)
    cursor.execute(func.delete_chosen_card(power))
