from peewee import *

db = SqliteDatabase('pizza_bot_database.sqlite')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    id = IntegerField(primary_key=True)
    status = CharField(column_name='status')
    name = CharField()
    username = CharField()


class Pizza(BaseModel):
    id = AutoField()
    name = CharField()
    price = IntegerField()


class Order(BaseModel):
    id = AutoField()
    status = CharField(default='В обработке')
    user = ForeignKeyField(User, backref='orders', on_delete='CASCADE')
    pizzas = CharField()
    address = TextField()
    phone = CharField()


db.create_tables([User, Pizza, Order])
