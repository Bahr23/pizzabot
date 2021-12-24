from models import *

orders = Order.select()
for o in orders:
    o.delete_instance()