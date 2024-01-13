import json
import psycopg2
import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from prettytable import PrettyTable 


PASSWORD = input('Введите пароль от базы данных: ')

Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)
    
    def __str__(self):
        return f'{self.name}'

class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=160), unique=True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)
    publisher = relationship(Publisher, backref="books")
    
    def __str__(self):
        return f'{self.title}'


class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)
    
    def __str__(self):
        return f'{self.name}'


class Stock(Base):
    __tablename__ = "stock"

    id = sq.Column(sq.Integer, primary_key=True)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    shop = relationship(Shop, backref="sto")
    book = relationship(Book, backref="stocks")
    
    def __str__(self):
        return f'{self.count}'
    
    
class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.DateTime, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=False)
    stock = relationship(Stock, backref="stocks")
    
    def __str__(self):
        return f'{self.price}, {self.date_sale}'


def create_tables(engine):
    #Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

#Создание адреса базы данных
DSN = f"postgresql://postgres:{PASSWORD}@localhost:5432/one_else"
engine = sqlalchemy.create_engine(DSN)
create_tables(engine)


#Создание сессии
Session = sessionmaker(bind = engine)
session = Session()


# =============================================================================
# #Заполнение базы данных
# with open(r"tests_data.json", "r", encoding="utf-8") as f:
#     data = json.load(f)
#     #pprint((data))
# 
# for record in data:
#     model = {
#         'publisher': Publisher,
#         'shop': Shop,
#         'book': Book,
#         'stock': Stock,
#         'sale': Sale,
#     }[record.get('model')]
#     session.add(model(id=record.get('pk'), **record.get('fields')))
# session.commit()
# =============================================================================

def getshops(search): #Функция принимает обязательный параметр
    th = ['название книги', 'название магазина', 'стоимость покупки', 'дата покупки']
    q = session.query(Book, Shop, Sale, Publisher).select_from(Shop).\
    join(Stock).\
    join(Book).\
    join(Publisher).\
    join(Sale)
    if search.isdigit():
        search_publ = q.filter(Publisher.id == search).all()
    else:
        search_publ = q.filter(Publisher.name == search).all()
    lisa = []
    for i in search_publ:
        lisa.append(str(i.Book))
        lisa.append(str(i.Shop))
        lisa.append(str(i.Sale).split(', ')[0])
        lisa.append(str(i.Sale).split()[1])
    columns = len(th)
    table = PrettyTable(th)
    td_data = lisa[:]
    while td_data:
        table.add_row(td_data[:columns])
        td_data = td_data[columns:]
    print(table)
        
            
        
getshops("2")
session.close()

