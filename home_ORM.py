import json
import os
import psycopg2
import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from pprint import pprint


Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)
# =============================================================================
#     homeworks = relationship("Book", back_populates="publisher") 
#     """Можно использовать вместо publisher = relationship(Publisher, backref="publisher")
#        в классе Book, но прописав в Book publisher = relationship(Publisher, back_populates="book")
#     """
# =============================================================================
    def __str__(self):
        return f'{self.name}'

class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=160), unique=True)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)
    # course = relationship(Course, back_populates="homeworks")
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
DSN = "postgresql://postgres:Vostok72@localhost:5432/one_else"
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


#Поиск данных
def search_info():
    name = input('Введите фамилию искомого автора: ')
    print('название книги', 'название магазина', 'стоимость покупки', 'дата покупки', sep=' | ')
    q = session.query(Publisher).join(Book).join(Stock).join(Sale).join(Shop).filter(Publisher.name == name)
    print(q)
    for s in q.all():
        print(s.name)
        for bk in s.books:
            print("\t", bk.title)
            for st in bk.stocks:
                #print("\t", st.count)
                for sl in st.stocks:
                    print("\t", sl.price,"\n\t", sl.date_sale)
    

        
    

    

search_info()

session.close()