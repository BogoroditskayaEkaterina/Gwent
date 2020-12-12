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
                      Column('id', Integer, primary_key=True),
                      Column('name', String),
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
(1, 'Вернон Роше', 'Ближний бой', 'Северные королевства', 10, 'Невосприимчивость'),
(2, 'Ян Наталис', 'Ближний бой', 'Северные королевства', 10, 'Невосприимчивость'),
(3, 'Эстерад Тиссен', 'Ближний бой', 'Северные королевства', 10, 'Невосприимчивость'),
(4, 'Филиппа Эльхарт', 'Дальний бой', 'Северные королевства', 10, 'Невосприимчивость'),
(5, 'Реданский пехотинец', 'Ближний бой', 'Северные королевства', 1, 'нет'),
(6, 'Грёбаная пехтура', 'Ближний бой', 'Северные королевства', 1, 'Прочная связь'),
(7, 'Ярпен Зигрин', 'Ближний бой', 'Северные королевства', 2, 'нет'),
(8, 'Боец Синих Полосок', 'Ближний бой', 'Северные королевства', 4, 'Прочная связь'),
(9, 'Сигизмунд Дийкстра', 'Ближний бой', 'Северные королевства', 4, 'Шпион'),
(10, 'Принц Стеннис', 'Ближний бой', 'Северные королевства', 5, 'Шпион'),
(11, 'Зигфрид из Денесле', 'Ближний бой', 'Северные королевства', 5, 'нет'),
(12, 'Бьянка', 'Ближний бой', 'Северные королевства', 5, 'нет'),
(13, 'Шелдон Скаггс', 'Дальний бой', 'Северные королевства', 4, 'нет'),
(14, 'Сабрина Глевиссиг', 'Дальний бой', 'Северные королевства', 4, 'нет'),
(15, 'Рубайлы из Кринфрида', 'Дальний бой', 'Северные королевства', 5, 'Прочная связь'),
(16, 'Шеала де Тансервилль', 'Дальний бой', 'Северные королевства', 5, 'нет'),
(17, 'Кейра Мец', 'Дальний бой', 'Северные королевства', 5, 'нет'),
(18, 'Детмольд', 'Дальний бой', 'Северные королевства', 6, 'нет'),
(19, 'Каэдвенский осадный мастер', 'Осадные', 'Северные королевства', 1, 'Прилив сил'),
(20, 'Талер', 'Осадные', 'Северные королевства', 1, 'Шпион'),
(21, 'Лекарь Бурой Хоругви', 'Осадные', 'Северные королевства', 5, 'Медик'),
(22, 'Осадная башня', 'Осадные', 'Северные королевства', 6, 'нет'),
(23, 'Баллиста', 'Осадные', 'Северные королевства', 6, 'нет'),
(24, 'Требушет', 'Осадные', 'Северные королевства', 6, 'нет'),
(25, 'Катапульта', 'Осадные', 'Северные королевства', 8, 'Прочная связь')
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
DROP FUNCTION IF EXISTS insert_card(bigint, text, text, text, bigint, text);
CREATE FUNCTION insert_card(a1 bigint, a2 text, a3 text, a4 text, a5 bigint, a6 text)
RETURNS void
AS
$$
insert into cards values
(a1, a2, a3, a4, a5, a6)
$$Language sql;
'''

def insert_card(a1, a2, a3, a4, a5, a6):
    cursor.execute(query3)
    cursor.execute(func.insert_card(a1, a2, a3, a4, a5, a6))

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
create INDEX name ON cards (name);
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
DELETE FROM cards WHERE id = (SELECT id FROM cards ORDER BY id DESC LIMIT 1)
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
DROP FUNCTION IF EXISTS change_card(text, text);
CREATE FUNCTION change_card(new_name text, old_name text)
RETURNS void
AS
$$
UPDATE cards SET name = new_name where name = old_name ;
$$Language sql;
'''

def change_card(new_name, old_name):
    cursor.execute(query9)
    cursor.execute(func.change_card(new_name, old_name))

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
DROP FUNCTION IF EXISTS delete_chosen_card(bigint);
CREATE FUNCTION delete_chosen_card(id_card bigint)
RETURNS void
AS
$$
DELETE FROM cards WHERE id = id_card;
$$Language sql;
'''

def delete_chosen_card(id_card):
    cursor.execute(query12)
    cursor.execute(func.delete_chosen_card(id_card))

query13 = '''
DROP FUNCTION IF EXISTS delete_some_cards(text);
CREATE FUNCTION delete_chosen_card(str text)
RETURNS void
AS
$$
DELETE FROM cards
WHERE name LIKE str;
$$Language sql;
'''

def delete_some_cards(name):
    cursor.execute(query13)
    string = '%' + name + '%'
    cursor.execute(func.delete_chosen_card(string))